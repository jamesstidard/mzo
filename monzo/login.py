import sys
import secrets
import asyncio

from asyncio import Event, FIRST_COMPLETED
from urllib.parse import urlencode
from contextlib import redirect_stdout

import aioconsole
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
Your browser-of-choice should be opening ready to request authentication for this \
command line application to access your Monzo account.

If your browser has not opened, please manually browse to this link:

{url:}

Or hit [Enter] to terminate this process\
"""


@monzo.command(short_help='Authenticate application with your Monzo account.')
async def login():
    app = Sanic(__name__, configure_logging=False)
    nonce = secrets.token_urlsafe(32)
    oauth_complete = Event()

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
            click.echo(setter)
            oauth_complete.set()
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

    # All output needs to be over stderr for prompts to show in eval
    with redirect_stdout(sys.stderr):
        pretty_url = click.style(url, fg='blue', underline=True)
        click.echo(message=SERVER_KILL_PROMPT.format(url=pretty_url))

    user_killed = asyncio.Task(aioconsole.ainput())
    oauth_completed = asyncio.Task(oauth_complete.wait())

    done, _ = await asyncio.wait([user_killed, oauth_completed], return_when=FIRST_COMPLETED)

    if oauth_completed in done:
        message = click.style("Session Authenticated", fg='green')
    elif user_killed in done:
        message = click.style("Authentication Canceled", fg='red')
    else:
        message = click.style("Error", fg='red')

    with redirect_stdout(sys.stderr):
        click.echo(message=message)

