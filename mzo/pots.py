# -*- coding: utf-8 -*-
import uuid
import asyncio

import click

from fuzzywuzzy import process

import mzo.utils.authentication
from mzo.utils.formats import Format
from mzo.utils.emoji import STYLE_EMOJI, CURRENT_ACCOUNT_EMOJI


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
@click.option(
    "-y",
    "--yes",
    "auto_yes",
    help="Auto accept the confirmation prompt.",
    default=False,
    is_flag=True,
)
@mzo.options.fmt()
@mzo.utils.authentication.authenticated
async def move(ctx, amount, from_, into, auto_yes, fmt: Format):
    amount = int(amount * 100)

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

    # is the transfer feasible?
    if from_["balance"] < amount:
        click.echo(
            (
                f"Insufficient funds in {from_['name']}. "
                f"Balance: {from_['balance']/100:.2f}"
            ),
            color="red",
        )
        ctx.exit(1)
    else:
        final_from_balance = from_["balance"] - amount

    final_into_balance = into["balance"] + amount

    def emoji(location):
        if location == current_account:
            return CURRENT_ACCOUNT_EMOJI
        else:
            return STYLE_EMOJI[location["style"]]

    preview = [
        {
            "name": from_candidate_name,
            "emoji": emoji(from_),
            "current": f"{from_['balance']/100:.2f}",
            "final": f"{final_from_balance/100:.2f}",
        },
        {
            "name": into_candidate_name,
            "emoji": emoji(into),
            "current": f"{into['balance']/100:.2f}",
            "final": f"{final_into_balance/100:.2f}",
        },
    ]

    key_order = ["name", "current", "final"]
    justify_columns = {"current": "right", "final": "right"}

    if fmt is Format.human:

        def fmt_header(header):
            return click.style(header.title(), bold=True)

        key_order = [fmt_header(k) for k in key_order]
        justify_columns = {fmt_header(k): v for k, v in justify_columns.items()}

        preview = [
            {
                # replace row item's keys with header keys and
                # concat emoji to name value
                fmt_header(k): f'{r["emoji"]} {v}' if k == "name" else v
                for k, v in r.items()
            }
            for r in preview
        ]

    output = fmt.dumps(preview, keys=key_order, justify_columns=justify_columns)
    click.echo(output)

    click.confirm(
        "\nConfirm this transfer", default=False, show_default=True, abort=True, err=True
    )

    if from_ != current_account:
        withdraw_resp = await ctx.obj.http.put(
            url=f"https://api.monzo.com/pots/{from_['id']}/withdraw",
            data={
                "destination_account_id": ctx.obj.account_id,
                "amount": amount,
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
                "amount": amount,
                "dedupe_id": uuid.uuid4().hex,
            },
        )
        if deposit_resp.status != 200:
            click.echo(
                f"Error trying to deposit to {into['name']}: {deposit_resp}",
                color="red",
            )
            ctx.exit(1)

    click.echo("Transfer successful!", color="green", err=True)


pots.add_command(move)
