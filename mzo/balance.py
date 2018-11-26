# -*- coding: utf-8 -*-
import asyncio

import click

import mzo.utils.authentication
from mzo.utils.formats import Format


@mzo.command(short_help='View account\'s current balance.')
@click.pass_context
@mzo.options.fmt()
@mzo.utils.authentication.authenticated
async def balance(ctx, fmt: Format):
    params = {'account_id': ctx.obj.account_id}

    get_balance = ctx.obj.http.get('https://api.monzo.com/balance', params=params)
    get_pots = ctx.obj.http.get('https://api.monzo.com/pots', params=params)

    balance_resp, pots_resp = await asyncio.gather(get_balance, get_pots)
    balance_json = await balance_resp.json()
    pots_json = await pots_resp.json()

    def style_emoji(p):
        return {
            'cassette': '📼',
            'balls': '🎾',
            'beach_ball': '🏖',
            'rain': '☔',
            'fairy_lights': '💡',
            'yacht': '⛵',
            'piggy_bank': '🐷',
            'window': '🏠',
        }.get(p['style'], '🍯')

    rows = [
        {
            'name': 'Current Account',
            'balance': f'{balance_json["balance"]/100:.2f}',
            'emoji': '💸',
        },
        *[{
            'name': p['name'],
            'balance': f'{p["balance"]/100}:.2f',
            'emoji': style_emoji(p)
        } for p in pots_json['pots'] if not p['deleted']],
        {
            'name': 'Total',
            'balance': f'{balance_json["total_balance"]/100}:.2f',
            'emoji': '💰',
        }
    ]

    key_order = ['name', 'balance']

    if fmt is Format.human:
        def fmt_header(header):
            return click.style(header.title(), bold=True)

        key_order = [fmt_header(k) for k in key_order]

        rows = [{
            # replace row item's keys with header keys and concat emoji to name value
            fmt_header(k): f'{r["emoji"]} {v}' if k == 'name' else v for k, v in r.items()}
            for r in rows]

        # Spacer between total row
        rows.insert(-1, dict.fromkeys(key_order, ''))

    output = fmt.dumps(rows, keys=key_order)
    click.echo(output)
