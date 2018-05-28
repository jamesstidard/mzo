import click

import monzo


@monzo.group()
@click.pass_context
@monzo.options.account_id()
@monzo.options.access_token()
async def cli(ctx, account_id, access_token):
    ctx.obj = monzo.UserData(
        account_id=account_id,
        access_token=access_token
    )


cli.add_command(monzo.accounts)
cli.add_command(monzo.balance)
cli.add_command(monzo.pay)


if __name__ == '__main__':
    cli()
