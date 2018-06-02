import click


class ContextObject:

    def __init__(self, *, http, app_dir, account_id, access_token):
        self.http = http
        self.app_dir = app_dir
        self.account_id = account_id
        self.access_token = access_token


from monzo.utils import group, command
from monzo import types, arguments, options
from monzo.accounts import accounts
from monzo.balance import balance
from monzo.pay import pay
from monzo.login import login
from monzo.logout import logout
