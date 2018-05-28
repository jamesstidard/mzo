from functools import partial

import click

import monzo


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
    type=monzo.types.FloatRange(min=0),
    metavar='<amount>',
)
