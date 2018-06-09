
OAUTH_REDIRECT_URI = 'http://localhost:40004/oauth'


class ContextObject:

    def __init__(self, *, http, app_dir, client_id, client_secret, account_id, access_token):
        self.http = http
        self.app_dir = app_dir
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.access_token = access_token


from monzo.utils import group, command
from monzo import types, arguments, options
from monzo.accounts import accounts
from monzo.balance import balance
from monzo.login import login
from monzo.logout import logout
from monzo.pay import pay
