import mz


@mz.group()
def cli():
    pass


cli.add_command(mz.pay)


if __name__ == '__main__':
    cli()
