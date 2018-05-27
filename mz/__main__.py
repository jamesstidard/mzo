from mz.pay import pay
from mz.utils import group


@group()
def cli():
    pass


cli.add_command(pay)


if __name__ == '__main__':
    cli()
