import aiohttp

import mz


@mz.command(short_help='View account\'s current balance.')
@mz.pass_user_data
async def balance(user_data):
    url = 'https://api.monzo.com/balance'
    headers = {'Authorization': f'Bearer {user_data.access_token}'}
    params = {'account_id': user_data.account_id}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as resp:
            print(resp.status)
            print(await resp.text())
