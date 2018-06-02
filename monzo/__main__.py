import os
import asyncio
import uvloop
import click
import toml
import monzo
import aiohttp

from functools import partial

from monzo.utils import wait

asyncio.set_event_loop(uvloop.new_event_loop())


@monzo.group()
@click.pass_context
@monzo.options.account_id()
@monzo.options.access_token()
async def cli(ctx, account_id, access_token):
    # Override defaults with config defaults
    app_dir = click.get_app_dir('monzo', force_posix=True)
    config_fp = os.path.join(app_dir, 'config')
    try:
        config = toml.load(config_fp)
    except FileNotFoundError:
        pass
    except toml.TomlDecodeError:
        click.echo(f'Unable to read config file "{config_fp}". Make sure it is valid TOML.')
        ctx.exit()
    else:
        if not account_id:
            account_id = config.get('default', {}).get('account_id')

    app_dir = click.get_app_dir('monzo', force_posix=True)

    headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
    session = aiohttp.ClientSession(headers=headers)
    ctx.call_on_close(partial(wait, session.close()))

    ctx.obj = monzo.ContextObject(
        http=session,
        app_dir=app_dir,
        account_id=account_id,
        access_token=access_token,
    )


cli.add_command(monzo.login)
cli.add_command(monzo.logout)
cli.add_command(monzo.accounts)
cli.add_command(monzo.balance)
cli.add_command(monzo.pay)


def main():
    cli()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
