""" main.py docstring
"""

import sys
import click
from loguru import logger

from src.utils_init import click_config_file,DEFAULT_LOG_LEVEL
from src.build import build
from src.deploy import deploy
from src.check import check

logger.remove()
logger.add(sys.stderr, level=DEFAULT_LOG_LEVEL)


# might be handy to open/close the DB before/after the group
#  https://click.palletsprojects.com/en/8.1.x/advanced/#managing-resources


@click.group(help="DBC - send commands to database",invoke_without_command=True)
@click.option('--log-level',
    default=DEFAULT_LOG_LEVEL,
#    default="TRACE",
    type=click.Choice(['TRACE','DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL'],
    case_sensitive=False)
)
@click_config_file.configuration_option()
@click.pass_context
def cli(ctx,log_level):
    """ main cli """
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    if log_level != DEFAULT_LOG_LEVEL:
        logger.info(f"Log level changed to: {log_level}" )
    else:
        logger.debug(f"Default log level: {DEFAULT_LOG_LEVEL}")

    if ctx.invoked_subcommand is None:
        logger.info("No command provided. Invoking help.")
        click.echo( ctx.get_help() )
    else:
        logger.debug(f"Invoking (from main) {ctx.invoked_subcommand}")


cli.add_command(build.build)
cli.add_command(deploy.deploy)
cli.add_command(check)

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter
