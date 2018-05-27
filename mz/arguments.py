from functools import partial

import click


name = partial(
    click.argument,
    'name',
    nargs=-1,
    metavar='<recipient-name>...',
)

amount = partial(
    click.argument,
    'amount',
    nargs=1,
    type=float,
    metavar='<amount>',
)
