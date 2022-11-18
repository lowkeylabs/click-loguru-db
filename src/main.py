import click
import sys
from loguru import logger


if __name__ == '__main__':
    from build import build
    from deploy import deploy
    from check import check
    from utils_init import *
else:
    from .build import build
    from .deploy import deploy
    from .check import check
    from .utils_init import *


# might be handy to open/close the DB before/after the group
#  https://click.palletsprojects.com/en/8.1.x/advanced/#managing-resources


@click.group(help="DBC - send commands to database",invoke_without_command=True)
@click.option('--log-level',
    default=default_log_level,
    type=click.Choice(['TRACE','DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL'],
    case_sensitive=False)
)
@click_config_file.configuration_option(implicit=True,provider=myprovider)
@click.pass_context
def cli(ctx,log_level):
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    if ctx.invoked_subcommand is None:
        logger.info(f"No command provided. Invoking help.")
        click.echo( ctx.get_help() )
    else:
        logger.info(f"Invoking (from main) {ctx.invoked_subcommand}")
        pass
    click.echo(f"parameter log_level: {log_level}" )
    pass


cli.add_command(build.build)
cli.add_command(deploy.deploy)
cli.add_command(check)

if __name__ == '__main__':
    cli()
