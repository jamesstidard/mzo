import sys
import secrets
import asyncio

from asyncio import FIRST_COMPLETED
from contextlib import redirect_stdout

import aioconsole
import click

import monzo

from monzo.oauth_server import OAuthServer

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
    nonce = secrets.token_urlsafe(32)
    server = OAuthServer(nonce=nonce)
    auth_url = server.auth_request_url

    click.launch(auth_url)

    # All output needs to be over stderr for prompts to show in eval
    with redirect_stdout(sys.stderr):
        pretty_url = click.style(auth_url, fg='blue', underline=True)
        click.echo(message=SERVER_KILL_PROMPT.format(url=pretty_url))

    await server.run()

    user_killed = asyncio.Task(aioconsole.ainput())
    access_token = asyncio.Task(server.access_token())

    completed, _ = await asyncio.wait([user_killed, access_token], return_when=FIRST_COMPLETED)

    if access_token in completed:
        message = click.style("Session Authenticated", fg='green')
    elif user_killed in completed:
        message = click.style("Authentication Canceled", fg='red')
    else:
        message = click.style("Error", fg='red')

    with redirect_stdout(sys.stderr):
        click.echo(message=message)

