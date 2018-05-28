import secrets

from urllib.parse import urlencode

import aiohttp
import click
import aioconsole

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import Unauthorized

import monzo


CLIENT_ID = 'oauthclient_00009QgEkW8zP76s4rwEDZ'
CLIENT_SECRET = 'nf8XwQJa/Tx87EU8pny5OUTHtAf4jch6fv9XxRCn/aRdsEUU02EcTow6+Cod+fJ2VvI7B9UMGWh6sozJgamZ'
REDIRECT_URI = 'http://localhost:40004/welcome-back'
RESPONSE_TYPE = 'code'


@monzo.command(short_help='Authenticate application with your Monzo account.')
async def login():
    app = Sanic(__name__)
    nonce = secrets.token_urlsafe(32)

    @app.route("/welcome-back")
    async def test(request):
        if request.args['state'][0] != nonce:
            raise Unauthorized("The nonce returned from Monzo does not match the one sent out.")

        async with aiohttp.ClientSession() as session:
            resp = await session.post('https://api.monzo.com/oauth2/token', data={
                'grant_type': 'authorization_code',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'code': request.args['code'][0]})
            print(await resp.json())
            return json('done')

    _ = await app.create_server(host='localhost', port=40004, access_log=False)

    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': RESPONSE_TYPE,
        'state': nonce,
    }

    url = f'https://auth.monzo.com?{urlencode(params)}'
    click.launch(url)
    await aioconsole.ainput(
        f'Your browser-of-choice should be opening ready to request authentication for this '
        f'command line application to access your Monzo account.\n'
        f'\n'
        f'If your browser has not opened, please manually browse to this link:\n'
        f'\n'
        f'{url}\n'
        f'\n'
        f'Or hit [Enter] to terminate this process.\n')
    print('done')
