import sys

from contextlib import redirect_stdout

import click

import monzo

from monzo.utils import ENV_SETTER


@monzo.command(short_help='Logout of authenticated session.')
async def logout():
    click.echo(ENV_SETTER.format(name='MONZO_ACCESS_TOKEN', value=""))

    with redirect_stdout(sys.stderr):
        message = click.style(f"Logged Out", fg='green')
        click.echo(message=message)