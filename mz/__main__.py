import click

from mz.pay import pay


@click.group()
def cli():
    pass


cli.add_command(pay)


if __name__ == '__main__':
    cli()
