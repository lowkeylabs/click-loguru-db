""" module check.py
"""
import os
import click
from loguru import logger
from src import click_config_file

logger.trace(f"After imports {__file__}")

@click.command()
@click.option('--quick', is_flag=True, help='Perform checking function without module')
@click.option('--test',  default="test string in click.option", help='reading a string')
#@click_config_file.configuration_option(implicit=True,provider=myprovider)
@click_config_file.configuration_option()
def check(quick,test):
    """ Command check docstring """
    logger.info("Entering command check")
    if quick:
        print('Quick form checking ...')
    else:
        print('Long form checking ...')

    click.echo(f"parameter test: {test}" )
    click.echo(f"parameter quick: {quick}" )
    click.echo(f"current folder:{os.getcwd()}")

if __name__ == '__main__':
    check() # pylint: disable=no-value-for-parameter
