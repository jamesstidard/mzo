# -*- coding: utf-8 -*-

import asyncio

import click
import aiohttp

import mzo


@mzo.command(short_help='View account\'s current balance.')
@mzo.pass_user_data
async def balance(user_data):
    headers = {'Authorization': f'Bearer {user_data.access_token}'}
    params = {'account_id': user_data.account_id}

    async with aiohttp.ClientSession(headers=headers) as session:
        get_balance = session.get('https://api.monzo.com/balance', params=params)
        get_pots = session.get('https://api.monzo.com/pots', params=params)

        balance_resp, pots_resp = await asyncio.gather(get_balance, get_pots)
        balance_json = await balance_resp.json()
        pots_json = await pots_resp.json()

        total_balance = f"💰 Total: {balance_json['total_balance']/100}"
        current_balance = f"💸 Current: {balance_json['balance']/100}"
        pots_balance = [
            f"🍯 {p['name']}: {p['balance']/100}"
            for p in pots_json['pots']
            if not p['deleted']]

        click.echo("\n".join([current_balance, *pots_balance, f"\n{total_balance}"]))
