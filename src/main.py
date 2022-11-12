import click

if __name__ == '__main__':
    from build import build
    from deploy import deploy
    from check import check
else:
    from .build import build
    from .deploy import deploy
    from .check import check

@click.group(help="CLI tool to manage full development cycle of projects")
def cli():
    pass


cli.add_command(build.build)
cli.add_command(deploy.deploy)
cli.add_command(check)

if __name__ == '__main__':
    cli()
