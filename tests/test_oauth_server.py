import pytest
import aiohttp

from mzo.utils.oauth_server import OAuthServer


@pytest.mark.asyncio
async def test_server_run():
    session = aiohttp.ClientSession()
    server = OAuthServer(
        client_id="client_id",
        client_secret="secret",
        nonce="nonce",
        http_session=session,
    )
    await server.run()
