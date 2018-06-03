import os
import asyncio

from collections import Awaitable
from functools import wraps, partial

import toml
import click
import aiohttp
import nacl.hash
import nacl.secret
import nacl.encoding
import nacl.exceptions



ENV_SETTER = """\
export {name:}="{value:}"
# This command is meant to be used with your shell's eval function.
# Run 'eval $(monzo login)' to sign into your Monzo account.
"""


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return wait(result)
    return wrapper


def command(name=None, cls=None, options_metavar='[options]', **attrs):
    def decorator(f):
        f = async_command(f)
        return click.command(name=name, cls=cls, options_metavar=options_metavar, **attrs)(f)
    return decorator


def group(name=None, options_metavar='[options]', **attrs):
    def decorator(f):
        f = async_command(f)
        return click.group(name=name, options_metavar=options_metavar, **attrs)(f)
    return decorator


def wait(f):
    if isinstance(f, Awaitable):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f)
    else:
        return f


def authenticated(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        access_token = ctx.obj.access_token
        credentials_fp = os.path.join(ctx.obj.app_dir, 'credentials')

        if access_token:
            resp = await ctx.obj.http.get('https://api.monzo.com/ping/whoami')
        elif os.path.exists(credentials_fp):
            with open(credentials_fp, 'rb') as fp:
                cipher_text = fp.read()

            while True:
                password = click.prompt("Password", hide_input=True, err=True)
                secret_key = nacl.hash.sha256(password.encode('utf-8'), encoder=nacl.encoding.RawEncoder)
                secret_box = nacl.secret.SecretBox(secret_key)
                try:
                    plain_text = secret_box.decrypt(cipher_text)
                except nacl.exceptions.CryptoError:
                    click.echo("Incorrect Password", err=True, color='red')
                else:
                    del password, secret_key, secret_box
                    access_data = toml.loads(plain_text.decode('utf-8'))
                    access_token = access_data['access_token']

                    headers = {'Authorization': f'Bearer {access_token}'}
                    session = aiohttp.ClientSession(headers=headers)
                    sync_close = partial(wait, session.close())

                    ctx.call_on_close(sync_close)
                    ctx.obj.http = session
                    ctx.obj.access_token = access_token

                    resp = await ctx.obj.http.get('https://api.monzo.com/ping/whoami', headers={
                        'Authorization': f'Bearer {access_token}'})
                    break
        else:
            resp = None

        if not resp or resp.status == 401:
            if resp:
                payload = await resp.json()
                click.echo(payload['message'], err=True, color='red')

            click.echo('You are not logged in. See `monzo login --help`.', err=True, color='red')
            ctx.exit()

        return await f(*args, **kwargs)
    return wrapper
