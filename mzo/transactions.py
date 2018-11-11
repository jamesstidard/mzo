# -*- coding: utf-8 -*-
import click

from dateutil.parser import parse as iso8601_parse

import mzo.utils.authentication
from mzo.utils.formats import Format


@mzo.command(short_help='View account\'s current balance.')
@click.pass_context
@mzo.options.fmt()
@mzo.utils.authentication.authenticated
async def transactions(ctx, fmt: Format):
    params = {'account_id': ctx.obj.account_id, 'expand[]': 'merchant'}

    resp = await ctx.obj.http.get('https://api.monzo.com/transactions', params=params)
    payload = await resp.json()
    key_order = ['created', 'name', 'amount', 'category']
    transactions_ = [{
        'created': t['created'],
        'name': f"{t['merchant']['name']}" if t['merchant'] else t['description'],
        'amount': t['amount'] / 100,
        'category': t['category'].replace('_', ' ').title(),
    } for t in payload['transactions']]

    if fmt is Format.human:
        def fmt_row(key, value):
            if key == 'amount':
                if value and value > 0:
                    value = f'{value:+.2f}'
                    value = click.style(str(value), fg='green')
                elif value:
                    value = f'{abs(value):.2f}'
            if key == 'created':
                if value:
                    value = f'{iso8601_parse(value):%a %d %B}'

            return click.style(key.title(), bold=True), value

        transactions_ = (dict(fmt_row(k, v) for k, v in t.items()) for t in transactions_)
        key_order = [fmt_row(k, None)[0] for k in key_order]

    output = fmt.dumps(transactions_, keys=key_order)
    click.echo(output)

