import asyncio
import os
import secrets
import sys
from asyncio import FIRST_COMPLETED
from contextlib import redirect_stdout

import aioconsole
import click
import nacl.exceptions
import toml

import mzo
from mzo.utils import ENV_SETTER
from mzo.utils.authentication import (
    ExpiredAccessToken,
    refresh_access_data,
    test_access_token,
)
from mzo.utils.crypto import decrypt, encrypt
from mzo.utils.oauth_server import OAuthServer

OAUTH_APPLICATION_PROMPT = f"""\
Monzo currently have a limit on how many users a single developer can have \
using their applications (like this one) to 20 users.

To get around this you can instead register as a developer and become your \
own user. Here are the configuration details you will need:

             Name: Monzo CLI
         Logo URL: <blank>
    Redirect URLs: {mzo.OAUTH_REDIRECT_URI}
      Description: Command-line application for Monzo.
  Confidentiality: Confidential

Once completed you will be given a Client ID and a Client Secret which you \
can return here with.
"""

MONZO_OAUTH_CLIENT_CONSOLE_URL = "https://developers.monzo.com/apps/home"


MANUAL_BROWSER_PROMPT = """
    If your browser has not opened, please manually browse to this link:
    {url:}
"""


OAUTH_PROMPT = """\
Now that you've registered this application as your own you need to log in as \
your own first user.

Your Client ID and Secret will be saved so you will not need to provide this \
them again in future.
"""


SERVER_KILL_PROMPT = """\
Please complete the authentication process in the browser to grant this \
application access to your account.

Or hit [ENTER] to terminate this process.
"""

PASSWORD_PROMPT = """\
We want to make sure anyone using your machine can not just send themselves \
all your money, let's add a password. Keep it secret, keep it safe.
"""


@mzo.command(short_help="Authorization & session management")
@click.option(
    "-f",
    "--format",
    "fmt",
    type=click.Choice(["raw", "cmd"]),
    default="cmd",
    help="Chose the format the access token is return in.",
)
@click.option(
    "--reauthorize",
    is_flag=True,
    help="Reauthorize the application's access to your Monzo account.",
)
@click.pass_context
async def login(ctx, reauthorize, fmt):
    """
    Manages authorizing this application to access your Monzo account as well \
    as creating authenticated sessions.

    This function should be called within your shell's eval statement for the \
    login session to be persisted.

    \b
    Authorization:

    The first time this command is called (or when it is subsequently called with the
    --reauthorize flag), the application request access to your Monzo account via OAuth.
    This will involve navigating you to the Monzo website to grant this application
    permissions to access your account by providing this application with a application-specific
    access token for your account.

    Once granted access, you will be prompted for a password to encrypt the access token
    so it can be stored securely on your machine and prevent anyone with access to your machine
    being able to have unfettered access to your Monzo account.

    \b
    Authenticated Sessions:

    After the application has been authorized to access your Monzo accounts calls to
    this command will give the ability to create a persisted login session within your
    terminal. This means that your password will not be needed for all commands executed
    within that session. This is done by decrypting the access token with your provided
    password and storing it in memory as a environment variable on the machine (aptly named:
    MZO_ACCESS_TOKEN).

    For convince this command will return the required shell command to set the environment
    variable (e.g. `export MZO_ACCESS_TOKEN="xxx"`) which means you can call this function
    within your shell's eval command so the above statement is executed for you and the
    environment variable set. However you may be using a shell that doesn't use the above syntax
    or want to manage the token yourself, in which case providing the `--format raw` will simply
    return the value of the access token instead of the shell command.
    """
    credentials_fp = os.path.join(ctx.obj.app_dir, "credentials")
    have_credentials = os.path.isfile(credentials_fp)

    if reauthorize or not have_credentials:
        stderr_echo(OAUTH_APPLICATION_PROMPT)
        _ = click.prompt(
            text="Hit [ENTER] to open browser to developer console where you can register your own application",
            default="done",
            hide_input=True,
            show_default=False,
            err=True,
        )

        click.launch(MONZO_OAUTH_CLIENT_CONSOLE_URL)
        stderr_echo(
            MANUAL_BROWSER_PROMPT.format(url=style_url(MONZO_OAUTH_CLIENT_CONSOLE_URL))
        )

        ctx.obj.client_id = click.prompt("Client ID", err=True)
        ctx.obj.client_secret = click.prompt("Client Secret", err=True)
        stderr_echo("\nPerfect!\n", color="green")

        access_data = await authorize(ctx)
        ctx.obj.access_token = access_data["access_token"]
        default_account = await select_default_account(ctx)

        click.echo(PASSWORD_PROMPT, err=True)
        password = click.prompt(
            "Password", err=True, confirmation_prompt=True, hide_input=True
        )
        encrypted_access_data = encrypt(
            toml.dumps(access_data).encode("utf-8"), password=password
        )

        os.makedirs(ctx.obj.app_dir, exist_ok=True)

        with open(os.path.join(ctx.obj.app_dir, "credentials"), "wb+") as fp:
            fp.write(encrypted_access_data)

        with open(os.path.join(ctx.obj.app_dir, "config"), "w+") as fp:
            toml.dump(
                {
                    "default": {
                        "account_id": default_account["id"],
                        "format": "human",
                    },
                    "oauth": {
                        "client_id": ctx.obj.client_id,
                        "client_secret": ctx.obj.client_secret,
                    },
                },
                fp,
            )

        stderr_echo(f"Client Authorized", color="green")
    else:
        with open(credentials_fp, "rb") as fp:
            cipher_text = fp.read()

        while True:
            password = click.prompt("Password", hide_input=True, err=True)
            try:
                plain_text = decrypt(cipher_text, password=password)
            except nacl.exceptions.CryptoError:
                click.echo("Incorrect Password", err=True, color="red")
            else:
                access_data = toml.loads(plain_text.decode("utf-8"))

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
                finally:
                    break

    if fmt == "raw":
        click.echo(access_data["access_token"])
    else:
        stderr_echo(f"Login Session Active", color="green")
        click.echo(
            ENV_SETTER.format(
                name="MZO_ACCESS_TOKEN", value=access_data["access_token"]
            )
        )


def stderr_echo(message, color=None, underline=False):
    """ All output needs to be over stderr for prompts to show in eval. """
    message = click.style(message, fg=color, underline=underline)
    with redirect_stdout(sys.stderr):
        click.echo(message=message)


def style_url(url):
    return click.style(url, fg="blue", underline=True)


async def authorize(ctx):
    nonce = secrets.token_urlsafe(32)
    server = OAuthServer(
        client_id=ctx.obj.client_id,
        client_secret=ctx.obj.client_secret,
        nonce=nonce,
        http_session=ctx.obj.http,
    )

    stderr_echo(OAUTH_PROMPT)
    _ = click.prompt(
        text="Hit [ENTER] to open your browser to authenticate this application to your Monzo account",
        default="done",
        hide_input=True,
        show_default=False,
        err=True,
    )

    click.launch(server.auth_request_url)
    pretty_url = style_url(server.auth_request_url)
    stderr_echo(
        MANUAL_BROWSER_PROMPT.format(url=pretty_url) + "\n" + SERVER_KILL_PROMPT
    )

    server_errors = asyncio.Task(server.run())
    user_killed = asyncio.Task(aioconsole.ainput())
    got_access_token = asyncio.Task(server.access_token())

    completed, _ = await asyncio.wait(
        [server_errors, user_killed, got_access_token], return_when=FIRST_COMPLETED
    )

    if got_access_token in completed:
        return got_access_token.result()
    elif user_killed in completed:
        stderr_echo("Authentication Canceled", color="red")
        ctx.exit(0)
    else:
        stderr_echo("Error", color="red")
        ctx.exit(1)


async def select_default_account(ctx):
    url = "https://api.monzo.com/accounts"
    headers = {"Authorization": f"Bearer {ctx.obj.access_token}"}

    resp = await ctx.obj.http.get(url, headers=headers)
    accounts = (await resp.json())["accounts"]
    accounts = [a for a in accounts if not a["closed"]]

    if len(accounts) > 1:
        raise NotImplementedError("cant handle multiple accounts currently")
    else:
        return accounts[0]
