# -*- coding: utf-8 -*-

import asyncio

import click
import aiohttp

import mz


@mz.command(short_help='View account\'s current balance.')
@mz.pass_user_data
async def balance(user_data):
    headers = {'Authorization': f'Bearer {user_data.access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        get_balance = session.get(
            'https://api.monzo.com/balance',
            params={'account_id': user_data.account_id})
        get_pots = session.get(
            'https://api.monzo.com/pots',
            params={'account_id': user_data.account_id})

        balance_resp, pots_resp = await asyncio.gather(get_balance, get_pots)
        balance_json = await balance_resp.json()
        pots_json = await pots_resp.json()

        total_balance = f"Σ Total: {balance_json['total_balance']/100}\n"
        current_balance = f"💰 Current: {balance_json['balance']/100}"
        pots_balance = "\n".join([
            f"🍯 {p['name']}: {p['balance']/100}"
            for p in pots_json['pots']
            if not p['deleted']])

        click.echo_via_pager("\n".join([total_balance, current_balance, pots_balance]))
