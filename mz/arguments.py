from functools import partial

import click

from mz import types


name = partial(
    click.argument,
    'name',
    nargs=-1,
    metavar='<recipient-name>...',
    callback=lambda ctx, param, value: ' '.join(value),
)


amount = partial(
    click.argument,
    'amount',
    nargs=1,
    type=types.FloatRange(min=0),
    metavar='<amount>',
)
