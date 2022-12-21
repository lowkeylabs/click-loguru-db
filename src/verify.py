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
    logger.info("Entering verify")
    if quick:
        print('Quick form verify ...')
    else:
        print('Long form verify ...')

    click.echo(f"parameter test: {test}" )
    click.echo(f"parameter quick: {quick}" )
    click.echo(f"current folder:{os.getcwd()}")

    click.echo(dumps(config))

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter
