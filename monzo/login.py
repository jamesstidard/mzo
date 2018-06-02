import sys
import secrets
import asyncio

from asyncio import FIRST_COMPLETED
from contextlib import redirect_stdout

import maya
import click
import aioconsole

import monzo

from monzo.oauth_server import OAuthServer
from monzo.utils import ENV_SETTER


SERVER_KILL_PROMPT = """\
Your browser-of-choice should be opening ready to request authentication for this \
command line application to access your Monzo account.

If your browser has not opened, please manually browse to this link:

{url:}

Or hit [Enter] to terminate this process
"""


@monzo.command(short_help='Authenticate application with your Monzo account.')
async def login():
    nonce = secrets.token_urlsafe(32)
    server = OAuthServer(nonce=nonce)

    click.launch(server.auth_request_url)

    # All output needs to be over stderr for prompts to show in eval
    with redirect_stdout(sys.stderr):
        pretty_url = click.style(server.auth_request_url, fg='blue', underline=True)
        click.echo(message=SERVER_KILL_PROMPT.format(url=pretty_url))

    await server.run()

    user_killed = asyncio.Task(aioconsole.ainput())
    got_access_token = asyncio.Task(server.access_token())

    completed, _ = await asyncio.wait([user_killed, got_access_token], return_when=FIRST_COMPLETED)

    if got_access_token in completed:
        access_data = got_access_token.result()
        access_token = access_data['access_token']
        expires = maya.now().add(seconds=access_data['expires_in'])
        click.echo(ENV_SETTER.format(name='MONZO_ACCESS_TOKEN', value=access_token))
        message = click.style(f"Session Authenticated [expires: {expires.slang_time()}]", fg='green')
    elif user_killed in completed:
        message = click.style("Authentication Canceled", fg='red')
    else:
        message = click.style("Error", fg='red')

    with redirect_stdout(sys.stderr):
        click.echo(message=message)
