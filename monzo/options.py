from functools import partial

import click


account_id = partial(
    click.option,
    '--account-id',
    metavar='<account-id>',
)

access_token = partial(
    click.option,
    '--access-token',
    metavar='<access-token>',
    envvar='MONZO_ACCESS_TOKEN',
)

sort_code = partial(
    click.option,
    '-s',
    '--sort-code',
    metavar='<00-00-00>',
    help='Sort code of the recipient.',
)

account_number = partial(
    click.option,
    '-a',
    '--account-number',
    metavar='<00000000>',
    help='Account number of the recipient.',
)

message = partial(
    click.option,
    '-m',
    '--message',
    metavar='<message>',
    help='Message for recipient to attach to the payment.',
)

on_datetime = partial(
    click.option,
    '--on',
    metavar='<date/time>',
    default='now',
    help='When the payment should be made on or reoccur from.',
)

daily_frequency_flag = partial(
    click.option,
    '--daily',
    'every',
    flag_value=(1, 'days'),
    help='Schedule payment to reoccur daily.',
)

weekly_frequency_flag = partial(
    click.option,
    '--weekly',
    'every',
    flag_value=(1, 'weeks'),
    help='Schedule payment to reoccur weekly.',
)

monthly_frequency_flag = partial(
    click.option,
    '--monthly',
    'every',
    flag_value=(1, 'months'),
    help='Schedule payment to reoccur monthly.',
)

yearly_frequency_flag = partial(
    click.option,
    '--yearly',
    'every',
    flag_value=(1, 'years'),
    help='Schedule payment to reoccur annually.',
)


NEVER = (0, 'days')

user_defined_frequency = partial(
    click.option,
    '--every',
    'every',
    metavar='<x> (days|weeks|months|years)',
    type=(int, click.Choice(['days', 'weeks', 'months', 'years'])),
    default=NEVER,
    help='Schedule payment to reoccur at given interval.',
)
