import click


class UserData:

    def __init__(self, account_id, access_token):
        self.account_id = account_id
        self.access_token = access_token


pass_user_data = click.make_pass_decorator(UserData)


from mzo.utils import group, command
from mzo import types, arguments, options
from mzo.accounts import accounts
from mzo.balance import balance
from mzo.pay import pay
