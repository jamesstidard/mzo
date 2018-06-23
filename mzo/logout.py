import sys

from contextlib import redirect_stdout

import click

import mzo

from mzo.utils import ENV_SETTER


@mzo.command(short_help='Logout of authenticated session.')
async def logout():
    click.echo(ENV_SETTER.format(name='MZO_ACCESS_TOKEN', value=""))

    with redirect_stdout(sys.stderr):
        message = click.style(f"Login Session Ended", fg='green')
        click.echo(message=message)
