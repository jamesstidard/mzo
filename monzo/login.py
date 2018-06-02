import secrets

from urllib.parse import urlencode
from functools import partial

import aiohttp
import click

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import Unauthorized

import monzo


CLIENT_ID = 'oauthclient_00009QgEkW8zP76s4rwEDZ'
CLIENT_SECRET = 'nf8XwQJa/Tx87EU8pny5OUTHtAf4jch6fv9XxRCn/aRdsEUU02EcTow6+Cod+fJ2VvI7B9UMGWh6sozJgamZ'
REDIRECT_URI = 'http://localhost:40004/welcome-back'
RESPONSE_TYPE = 'code'

ENV_SETTER = """\
export {name:}="{value:}"
# This command is meant to be used with your shell's eval function.
# Run 'eval $(monzo login)' to sign into your Monzo account.
"""

SERVER_KILL_PROMPT = """\
Your browser-of-choice should be opening ready to request authentication for this
command line application to access your Monzo account.

If your browser has not opened, please manually browse to this link:

{url:}

Or hit [Enter] to terminate this process"""


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
            payload = await resp.json()
            setter = ENV_SETTER.format(name='MONZO_ACCESS_TOKEN', value=payload['access_token'])
            click.echo(setter, err=True)
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
    user_kill = partial(
        click.confirm,
        text=SERVER_KILL_PROMPT.format(url=url),
        default=True,
        show_default=False,
        err=True)

    user_kill()
