# -*- coding: utf-8 -*-
import asyncio

import click

import monzo.utils.authentication
from monzo.utils.ascii_table import ascii_table


@monzo.command(short_help='View account\'s current balance.')
@click.pass_context
@monzo.utils.authentication.authenticated
async def balance(ctx):
    params = {'account_id': ctx.obj.account_id}

    get_balance = ctx.obj.http.get('https://api.monzo.com/balance', params=params)
    get_pots = ctx.obj.http.get('https://api.monzo.com/pots', params=params)

    balance_resp, pots_resp = await asyncio.gather(get_balance, get_pots)
    balance_json = await balance_resp.json()
    pots_json = await pots_resp.json()

    name_header = click.style('Name', bold=True)
    balance_header = click.style('Balance', bold=True)

    rows = [
        {
            name_header: '💸 Current Account',
            balance_header: balance_json['balance']/100,
        },
        *[{
            name_header: f"🍯 {p['name']}",
            balance_header: p['balance']/100,
        } for p in pots_json['pots'] if not p['deleted']],
        {
            # Spacing
        },
        {
            name_header: '💰 Total',
            balance_header: balance_json['total_balance']/100,
        }
    ]

    table = ascii_table(rows, columns=[name_header, balance_header], fill='')
    click.echo(table)
