""" module check.py
"""
import os
import click
from loguru import logger

#if __name__ == 'src.check':
#    from .utils_init import click_config_file
#else:

from src.utils_init import click_config_file

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
