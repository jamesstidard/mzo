import asyncio
from collections import Awaitable
from functools import wraps

import click

ENV_SETTER = """\
export {name:}="{value:}"
# This command is meant to be used with your shell's eval function.
# Run 'eval $(mzo login)' to sign into your Monzo account.
"""

NO_LOGIN_SESSION_ACTIVE = """\
No login session currently active. You can authorize this one-off command by providing your \
password, or see `mzo login --help` for persisting authentication between commands.
"""


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return wait(result)

    return wrapper


def command(name=None, cls=None, options_metavar="[options]", **attrs):
    def decorator(f):
        f = async_command(f)
        return click.command(
            name=name, cls=cls, options_metavar=options_metavar, **attrs
        )(f)

    return decorator


def group(name=None, options_metavar="[options]", **attrs):
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
