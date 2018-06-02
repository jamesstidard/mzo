import click


class UserData:

    def __init__(self, *, app_dir, account_id, access_token):
        self.app_dir = app_dir
        self.account_id = account_id
        self.access_token = access_token


pass_user_data = click.make_pass_decorator(UserData)


from monzo.utils import group, command
from monzo import types, arguments, options
from monzo.accounts import accounts
from monzo.balance import balance
from monzo.pay import pay
from monzo.login import login
from monzo.logout import logout
