import click

import mzo


@mzo.group()
@click.pass_context
@mzo.options.account_id()
@mzo.options.access_token()
async def cli(ctx, account_id, access_token):
    ctx.obj = mzo.UserData(
        account_id=account_id,
        access_token=access_token
    )


cli.add_command(mzo.accounts)
cli.add_command(mzo.balance)
cli.add_command(mzo.pay)


if __name__ == '__main__':
    cli()
