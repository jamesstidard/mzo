# -*- coding: utf-8 -*-
import asyncio

import click

import mzo.utils.authentication
from mzo.utils.formats import Format


@mzo.command(short_help="View account's current balance.")
@click.pass_context
@mzo.options.fmt()
@mzo.utils.authentication.authenticated
async def balance(ctx, fmt: Format):
    params = {
        "account_id": ctx.obj.account_id,
    }

    balance_req = ctx.obj.http.get(url="https://api.monzo.com/balance", params=params,)

    pots_req = ctx.obj.http.get(url="https://api.monzo.com/pots", params=params,)

    balance_resp, pots_resp = await asyncio.gather(balance_req, pots_req,)

    balance_, pots = await asyncio.gather(balance_resp.json(), pots_resp.json(),)

    def style_emoji(p):
        return {
            "cassette": "📼",
            "balls": "🎾",
            "beach_ball": "🏖",
            "rain": "☔",
            "fairy_lights": "💡",
            "yacht": "⛵",
            "piggy_bank": "🐷",
            "window": "🏠",
        }.get(p["style"], "🍯")

    rows = [
        {
            "name": "Current Account",
            "balance": f'{balance_["balance"]/100:.2f}',
            "emoji": "💸",
        },
        *[
            {
                "name": p["name"],
                "balance": f'{p["balance"]/100:.2f}',
                "emoji": style_emoji(p),
            }
            for p in pots["pots"]
            if not p["deleted"]
        ],
        {
            "name": "Total",
            "balance": f'{balance_["total_balance"]/100:.2f}',
            "emoji": "💰",
        },
    ]

    key_order = ["name", "balance"]
    justify_columns = {"balance": "right"}

    if fmt is Format.human:

        def fmt_header(header):
            return click.style(header.title(), bold=True)

        key_order = [fmt_header(k) for k in key_order]
        justify_columns = {fmt_header(k): v for k, v in justify_columns.items()}

        rows = [
            {
                # replace row item's keys with header keys and
                # concat emoji to name value
                fmt_header(k): f'{r["emoji"]} {v}' if k == "name" else v
                for k, v in r.items()
            }
            for r in rows
        ]

        # Spacer between total row
        rows.insert(-1, dict.fromkeys(key_order, ""))

    output = fmt.dumps(rows, keys=key_order, justify_columns=justify_columns)
    click.echo(output)
