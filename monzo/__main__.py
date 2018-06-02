import os
import asyncio
import uvloop
import click
import toml
import monzo

asyncio.set_event_loop(uvloop.new_event_loop())


@monzo.group()
@click.pass_context
@monzo.options.account_id()
@monzo.options.access_token()
async def cli(ctx, account_id, access_token):
    # Override defaults with config defaults
    config_fp = os.path.join(click.get_app_dir('monzo', force_posix=True), 'config')
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

    ctx.obj = monzo.UserData(
        config_path=config_fp,
        account_id=account_id,
        access_token=access_token
    )


cli.add_command(monzo.login)
cli.add_command(monzo.logout)
cli.add_command(monzo.accounts)
cli.add_command(monzo.balance)
cli.add_command(monzo.pay)


if __name__ == '__main__':
    cli()
