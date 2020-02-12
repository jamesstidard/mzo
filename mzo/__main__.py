import asyncio
import os
from functools import partial

import aiohttp
import click
import toml
import uvloop

import mzo
from mzo.utils import wait
from mzo.__version__ import __version__

asyncio.set_event_loop(uvloop.new_event_loop())


@mzo.group()
@click.version_option(__version__)
@click.pass_context
async def cli(ctx):
    app_dir = click.get_app_dir("mzo", force_posix=True)
    config_fp = os.path.join(app_dir, "config")

    client_id = None
    client_secret = None
    account_id = None
    access_token = os.environ.get("MZO_ACCESS_TOKEN")

    try:
        config = toml.load(config_fp)
    except FileNotFoundError:
        pass
    except toml.TomlDecodeError:
        click.echo(
            f'Unable to read config file "{config_fp}". ' "Make sure it is valid TOML."
        )
        ctx.exit()
    else:
        oauth = config.get("oauth", {})
        client_id = oauth.get("client_id")
        client_secret = oauth.get("client_secret")

        default = config.get("default", {})
        account_id = default.get("account_id")

    headers = None
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

    session = aiohttp.ClientSession(headers=headers)
    sync_close = partial(wait, session.close())
    ctx.call_on_close(sync_close)

    ctx.obj = mzo.ContextObject(
        http=session,
        app_dir=app_dir,
        client_id=client_id,
        client_secret=client_secret,
        account_id=account_id,
        access_token=access_token,
    )


cli.add_command(mzo.login)
cli.add_command(mzo.logout)
cli.add_command(mzo.balance)

if os.environ.get("MZO_PRERELEASE") == "1":
    cli.add_command(mzo.transactions)


def main():
    cli()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
