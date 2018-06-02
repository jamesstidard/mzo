import os
import sys
import secrets
import asyncio

from asyncio import FIRST_COMPLETED
from contextlib import redirect_stdout

import toml
import maya
import nacl.hash
import nacl.secret
import nacl.encoding
import click
import aiohttp
import aioconsole

import monzo

from monzo.utils import ENV_SETTER
from monzo.utils.oauth_server import OAuthServer


SERVER_KILL_PROMPT = """\
Your browser-of-choice should be opening ready to request authentication for this \
command line application to access your Monzo account.

If your browser has not opened, please manually browse to this link:

{url:}

Or hit [Enter] to terminate this process
"""

PASSWORD_PROMPT = """\
We want to make sure anyone using your machine can not just send themselves all your money, \
let's add a password. Make it strong.

Password\
"""


@monzo.command(short_help='Authenticate application with your Monzo account.')
@monzo.pass_user_data
async def login(user_data):
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
        access_data['expires_at'] = maya.now().add(seconds=access_data['expires_in'])

        password = click.prompt(PASSWORD_PROMPT, err=True, confirmation_prompt=True, hide_input=True)
        secret_key = nacl.hash.sha256(password.encode('utf-8'), encoder=nacl.encoding.RawEncoder)

        secret_box = nacl.secret.SecretBox(secret_key)
        encrypted_access_data = secret_box.encrypt(toml.dumps(access_data).encode('utf-8'))
        del password, secret_key

        os.makedirs(user_data.app_dir, exist_ok=True)
        with open(os.path.join(user_data.app_dir, 'credentials'), 'wb+') as fp:
            fp.write(encrypted_access_data)

        url = 'https://api.monzo.com/accounts'
        headers = {'Authorization': f'Bearer {access_data["access_token"]}'}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                accounts = (await resp.json())['accounts']
                accounts = [a for a in accounts if not a['closed']]

        if len(accounts) > 1:
            raise NotImplementedError('cant handle multiple accounts currently')
        else:
            os.makedirs(user_data.app_dir, exist_ok=True)
            with open(os.path.join(user_data.app_dir, 'config'), 'w+') as fp:
                toml.dump({'default': {'account_id': accounts[0]['id']}}, fp)

        click.echo(ENV_SETTER.format(name='MONZO_ACCESS_TOKEN', value=access_data["access_token"]))

        message = click.style(f'Session Authenticated [expires: {access_data["expires_at"].slang_time()}]', fg='green')
    elif user_killed in completed:
        message = click.style('Authentication Canceled', fg='red')
    else:
        message = click.style('Error', fg='red')

    with redirect_stdout(sys.stderr):
        click.echo(message=message)
