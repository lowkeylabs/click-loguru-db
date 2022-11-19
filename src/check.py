import click
import sys, os
from loguru import logger

if __name__ == 'src.check':
    from .utils_init import *
else:
    from utils_init import *

@click.command()
@click.option('--quick', is_flag=True, help='Perform checking function without module')
@click.option('--test',  default="test string in click.option", help='reading a string')
#@click_config_file.configuration_option(implicit=True,provider=myprovider)
@click_config_file.configuration_option()
def check(quick,test):
    """ Command check docstring """
    logger.info("Entering command check")
    if quick:
        print(f'Quick form checking ...')
    else:
        print(f'Long form checking ...')

    click.echo(f"parameter test: {test}" )
    click.echo(f"paramter quick: {quick}" )
    click.echo(f"current folder:{os.getcwd()}")

if __name__ == '__main__':
    check()

