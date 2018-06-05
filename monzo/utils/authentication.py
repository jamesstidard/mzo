import os
from functools import wraps, partial

import aiohttp
import click
import nacl.exceptions
import toml

from monzo import OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI
from monzo.utils import NO_LOGIN_SESSION_ACTIVE, wait
from monzo.utils.crypto import decrypt, encrypt


class ExpiredAccessToken(Exception):
    ...


def authenticated(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        access_token = ctx.obj.access_token
        credentials_fp = os.path.join(ctx.obj.app_dir, 'credentials')
        have_credentials = os.path.exists(credentials_fp)

        # Test access token from active login session works
        if access_token:
            try:
                await test_access_token(access_token, http_session=ctx.obj.http)
            except ExpiredAccessToken:
                # fall back to trying to refresh - will require user password
                if have_credentials:
                    with open(credentials_fp, 'rb') as fp_:
                        cipher_text = fp_.read()

                    password, access_data = retry_decrypt(cipher_text)
                    refresh_token = access_data['refresh_token']
                    access_data = await refresh_access_data(refresh_token, http_session=ctx.obj.http)
                    encrypted_access_data = encrypt(toml.dumps(access_data).encode('utf-8'), password=password)

                    with open(credentials_fp, 'wb+') as fp:
                        fp.write(encrypted_access_data)

                    click.echo('Your access token had expired, but has now been refreshed. '
                               'You will need to call `eval (monzo login)` again to update '
                               'your session value.', err=True, color='yellow')

                    access_token = access_data['access_token']
                else:
                    click.echo('Your access token had expired and there is no refresh token available. '
                           'Please reauthorize. See `monzo login --help`.', err=True, color='red')
                    raise click.Abort()

        # No session access token given, load from credentials file and test is it works
        elif have_credentials:
            click.echo(NO_LOGIN_SESSION_ACTIVE, err=True)

            with open(credentials_fp, 'rb') as fp_:
                cipher_text = fp_.read()

            password, access_data = retry_decrypt(cipher_text)

            try:
                await test_access_token(access_data['access_token'], http_session=ctx.obj.http)
            except ExpiredAccessToken:
                refresh_token = access_data['refresh_token']
                access_data = await refresh_access_data(refresh_token, http_session=ctx.obj.http)
                encrypted_access_data = encrypt(toml.dumps(access_data).encode('utf-8'), password=password)

                with open(credentials_fp, 'wb+') as fp:
                    fp.write(encrypted_access_data)

            access_token = access_data['access_token']

        # No access token from session or from credentials. Point user in right direction
        else:
            click.echo('You are not logged in. See `monzo login --help`.', err=True, color='red')
            raise click.Abort()

        # Recreate session with any updates to access_token
        headers = {'Authorization': f'Bearer {access_token}'}
        session = aiohttp.ClientSession(headers=headers)
        sync_close = partial(wait, session.close())

        # update ctx
        ctx.call_on_close(sync_close)
        ctx.obj.http = session
        ctx.obj.access_token = access_token

        return await f(*args, **kwargs)
    return wrapper


def retry_decrypt(cipher_text):
    while True:
        # Keep this password for later if we need to refresh and restore new credentials
        password = click.prompt("Password", hide_input=True, err=True)
        try:
            plain_text = decrypt(cipher_text, password=password)
        except nacl.exceptions.CryptoError:
            click.echo("Incorrect Password", err=True, color='red')
        else:
            plain_text = toml.loads(plain_text.decode('utf-8'))
            return password, plain_text


async def test_access_token(access_token, *, http_session):
    resp = await http_session.get(
        url='https://api.monzo.com/ping/whoami',
        headers={'Authorization': f'Bearer {access_token}'})

    if resp.status == 401:
        raise ExpiredAccessToken()


async def refresh_access_data(refresh_token, *, http_session):
    click.echo("Refreshing access token", err=True, color='green')
    resp = await http_session.post('https://monzo-cli.herokuapp.com/oauth2/token', data={
        'grant_type': 'refresh_token',
        'client_id': OAUTH_CLIENT_ID,
        'redirect_uri': OAUTH_REDIRECT_URI,
        'refresh_token': refresh_token})

    return await resp.json()
