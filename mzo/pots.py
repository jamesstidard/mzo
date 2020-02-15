# -*- coding: utf-8 -*-
import uuid
import asyncio

import click

from fuzzywuzzy import process

import mzo.utils.authentication
from mzo.utils.formats import Format


@click.group(short_help="View and manage your pots.")
def pots():
    pass


@mzo.command(short_help="Deposit/withdraw from your pots.")
@click.pass_context
@click.argument(
    "amount", type=click.FloatRange(min=0.01),
)
@click.option(
    "-f",
    "--from",
    "from_",
    type=str,
    help="The pot name to transfer from.",
    default="Current Account",
    show_default=True,
)
@click.option(
    "-t",
    "--into",
    "into",
    type=str,
    help="The pot name to transfer to.",
    default="Current Account",
    show_default=True,
)
@mzo.options.fmt()
@mzo.utils.authentication.authenticated
async def move(ctx, amount, from_, into, fmt: Format):
    params = {
        "account_id": ctx.obj.account_id,
    }

    balance_req = ctx.obj.http.get(url="https://api.monzo.com/balance", params=params)
    pots_req = ctx.obj.http.get(url="https://api.monzo.com/pots", params=params)

    balance_resp, pots_resp = await asyncio.gather(balance_req, pots_req)
    current_account, pots_data = await asyncio.gather(
        balance_resp.json(), pots_resp.json()
    )

    locations_by_name = dict(
        [
            ("Current Account", current_account),
            *(
                (p["name"], p)
                for p in pots_data["pots"]
                if not p["deleted"] and not p["locked"]
            ),
        ],
    )

    from_candidate_name, _ = process.extractOne(from_, locations_by_name.keys())
    into_candidate_name, _ = process.extractOne(into, locations_by_name.keys())

    from_ = locations_by_name[from_candidate_name]
    into = locations_by_name[into_candidate_name]

    if from_ == into:
        raise click.BadParameter(
            "Nothing to do: 'from' and 'into' appear to be the same location."
        )

    if from_ != current_account:
        withdraw_resp = await ctx.obj.http.put(
            url=f"https://api.monzo.com/pots/{from_['id']}/withdraw",
            data={
                "destination_account_id": ctx.obj.account_id,
                "amount": int(amount * 100),
                "dedupe_id": uuid.uuid4().hex,
            },
        )
        if withdraw_resp.status != 200:
            click.echo(
                f"Error trying to withdraw from {from_['name']}: {withdraw_resp}",
                color="red",
            )
            ctx.exit(1)

    if into != current_account:
        deposit_resp = await ctx.obj.http.put(
            url=f"https://api.monzo.com/pots/{into['id']}/deposit",
            data={
                "source_account_id": ctx.obj.account_id,
                "amount": int(amount * 100),
                "dedupe_id": uuid.uuid4().hex,
            },
        )
        if deposit_resp.status != 200:
            click.echo(
                f"Error trying to deposit to {into['name']}: {deposit_resp}",
                color="red",
            )
            ctx.exit(1)

    click.echo("done!", color="green")


pots.add_command(move)
