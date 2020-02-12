import os
from functools import wraps, partial

import aiohttp
import click
import nacl.exceptions
import toml

from mzo import OAUTH_REDIRECT_URI
from mzo.utils import NO_LOGIN_SESSION_ACTIVE, wait
from mzo.utils.crypto import decrypt, encrypt


class ExpiredAccessToken(Exception):
    ...


def authenticated(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        access_token = ctx.obj.access_token
        credentials_fp = os.path.join(ctx.obj.app_dir, "credentials")
        have_credentials = os.path.exists(credentials_fp)

        # Test access token from active login session works
        if access_token:
            try:
                await test_access_token(access_token, http_session=ctx.obj.http)
            except ExpiredAccessToken:
                # fall back to trying to refresh - will require user password
                if have_credentials:
                    click.echo(
                        "Your access token has expired."
                        "You will need to call `eval $(mzo login)` again to refresh "
                        "your token value.",
                        err=True,
                        color="red",
                    )
                    ctx.exit(1)
                else:
                    click.echo(
                        "Your access token had expired and there is no refresh token available. "
                        "Please reauthorize. See `mzo login --help`.",
                        err=True,
                        color="red",
                    )
                    raise click.Abort()

        # No session access token given, load from credentials file and test is it works
        elif have_credentials:
            click.echo(NO_LOGIN_SESSION_ACTIVE, err=True)

            with open(credentials_fp, "rb") as fp_:
                cipher_text = fp_.read()

            password, access_data = retry_decrypt(cipher_text)

            try:
                await test_access_token(
                    access_data["access_token"], http_session=ctx.obj.http
                )
            except ExpiredAccessToken:
                refresh_token = access_data["refresh_token"]
                access_data = await refresh_access_data(refresh_token, ctx=ctx)
                encrypted_access_data = encrypt(
                    toml.dumps(access_data).encode("utf-8"), password=password
                )

                with open(credentials_fp, "wb+") as fp:
                    fp.write(encrypted_access_data)

            access_token = access_data["access_token"]

        # No access token from session or from credentials. Point user in right direction
        else:
            click.echo(
                "You are not logged in. See `mzo login --help`.", err=True, color="red"
            )
            raise click.Abort()

        # Recreate session with any updates to access_token
        headers = {"Authorization": f"Bearer {access_token}"}
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
            click.echo("Incorrect Password", err=True, color="red")
        else:
            plain_text = toml.loads(plain_text.decode("utf-8"))
            return password, plain_text


async def test_access_token(access_token, *, http_session):
    resp = await http_session.get(
        url="https://api.monzo.com/ping/whoami",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if resp.status == 401:
        raise ExpiredAccessToken()


async def refresh_access_data(refresh_token, *, ctx):
    client_id = ctx.obj.client_id
    client_secret = ctx.obj.client_secret

    if not client_id or not client_secret:
        click.Abort("Unable to find oauth id and secret in config file.")
    else:
        resp = await ctx.obj.http.post(
            "https://api.monzo.com/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": OAUTH_REDIRECT_URI,
                "refresh_token": refresh_token,
            },
        )

        payload = await resp.json()

        if 200 <= resp.status < 300:
            return payload
        else:
            click.Abort(payload["message"])
