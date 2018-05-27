import click


class UserData:

    def __init__(self, account_id, access_token):
        self.account_id = account_id
        self.access_token = access_token


pass_user_data = click.make_pass_decorator(UserData)


from mz.utils import group, command
from mz import types, arguments, options
from mz.accounts import accounts
from mz.balance import balance
from mz.pay import pay
