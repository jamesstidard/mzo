import click

import mz


@mz.group()
@click.pass_context
@mz.options.account_id()
@mz.options.access_token()
async def cli(ctx, account_id, access_token):
    ctx.obj = mz.UserData(
        account_id=account_id,
        access_token=access_token
    )


cli.add_command(mz.accounts)
cli.add_command(mz.balance)
cli.add_command(mz.pay)


if __name__ == '__main__':
    cli()
