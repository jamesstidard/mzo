from asyncio import Event

from urllib.parse import urlencode

from sanic import Sanic
from sanic.response import text
from sanic.exceptions import Unauthorized

from monzo import OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI


class OAuthServer:

    def __init__(self, *, nonce, http_session):
        self.http = http_session
        self.app = Sanic(__name__, configure_logging=False)
        self.nonce = nonce
        self._oauth_complete = Event()
        self._access_token = None

        @self.app.route("/welcome-back")
        async def welcome_back(request):
            if request.args['state'][0] != self.nonce:
                raise Unauthorized("The nonce returned from Monzo does not match the one sent out.")

            resp = await self.http.post('https://monzo-cli.herokuapp.com/oauth2/token', data={
                'grant_type': 'authorization_code',
                'client_id': OAUTH_CLIENT_ID,
                'redirect_uri': OAUTH_REDIRECT_URI,
                'code': request.args['code'][0]})
            self._access_token = await resp.json()
            self._oauth_complete.set()
            return text('Authenticated.')

    @property
    def auth_request_url(self):
        params = {
            'client_id': OAUTH_CLIENT_ID,
            'redirect_uri': OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'state': self.nonce}
        return f'https://auth.monzo.com?{urlencode(params)}'

    async def run(self):
        await self.app.create_server(host='localhost', port=40004, access_log=False)

    async def access_token(self):
        await self._oauth_complete.wait()
        return self._access_token
