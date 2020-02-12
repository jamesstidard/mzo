from click.testing import CliRunner

from mzo.__main__ import cli


def test_authorize():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        args=["login"],
        input="""
client_id
secret
"""
    )
    assert result
