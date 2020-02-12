from collections import OrderedDict

import click

import mzo


@mzo.command(short_help="View all Monzo accounts.")
@click.pass_context
async def accounts(ctx):
    url = "https://api.monzo.com/accounts"
    headers = {"Authorization": f"Bearer {ctx.obj.access_token}"}

    resp = await ctx.obj.http.get(url, headers=headers)
    accounts_ = (await resp.json())["accounts"]

    choices = OrderedDict((a["id"], f"{a['description']}") for a in accounts_)
