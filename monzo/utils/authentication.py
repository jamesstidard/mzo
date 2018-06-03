import os
from functools import wraps, partial

import aiohttp
import click
import toml

from monzo.utils import NO_LOGIN_SESSION_ACTIVE, wait
from monzo.utils.crypto import decrypt


def authenticated(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        access_token = ctx.obj.access_token
        credentials_fp = os.path.join(ctx.obj.app_dir, 'credentials')

        if access_token:
            resp = await ctx.obj.http.get('https://api.monzo.com/ping/whoami')
        elif os.path.exists(credentials_fp):
            click.echo(NO_LOGIN_SESSION_ACTIVE, err=True)

            plain_text = decrypt(credentials_fp)
            access_data = toml.loads(plain_text.decode('utf-8'))
            access_token = access_data['access_token']

            headers = {'Authorization': f'Bearer {access_token}'}
            session = aiohttp.ClientSession(headers=headers)
            sync_close = partial(wait, session.close())

            ctx.call_on_close(sync_close)
            ctx.obj.http = session
            ctx.obj.access_token = access_token

            resp = await ctx.obj.http.get(
                url='https://api.monzo.com/ping/whoami',
                headers={'Authorization': f'Bearer {access_token}'})
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
