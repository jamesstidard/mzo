import aiohttp

import monzo


@monzo.command(short_help='View all Monzo accounts.')
@monzo.pass_user_data
async def accounts(user_data):
    url = 'https://api.monzo.com/accounts'
    headers = {'Authorization': f'Bearer {user_data.access_token}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            print(resp.status)
            accounts = await resp.json()
            print(accounts)
