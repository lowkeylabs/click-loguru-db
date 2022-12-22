""" module verify.py
"""
import os
import click
from loguru import logger
from src import click_config_file, myprovider

logger.trace(f"After imports {__file__}")

@click.command()
#@click_config_file.configuration_option()
@click_config_file.configuration_option(implicit=True,provider=myprovider)
def cli():
    """ Show PATH from environment """
    logger.debug(f"Entering {os.path.basename(__file__)[:-3]}")

    path = os.getenv("PATH")
    pieces = path.split(os.pathsep)
    for piece in pieces:
        click.echo(f"{piece}")

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter
