""" module verify.py
"""
import os
import click
from loguru import logger
from tomlkit import dumps
from src import click_config_file
from src import config

logger.trace(f"After imports {__file__}")

@click.command()
@click.option('--quick', is_flag=True, help='Perform checking function without module')
@click.option('--test',  default="test string in click.option", help='reading a string')
#@click_config_file.configuration_option(implicit=True,provider=myprovider)
@click_config_file.configuration_option()
def cli(quick,test):
    """ Command verify docstring """
    logger.debug(f"Entering {os.path.basename(__file__)[:-3]}")

    path = os.getenv("PATH")
    pieces = path.split(os.pathsep)
    for piece in pieces:
        click.echo(f"{piece}")

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter
