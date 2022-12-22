""" module verify.py
"""
import os
import click
from loguru import logger
from src import click_config_file,myprovider

logger.trace(f"After imports {__file__}")

@click.command()
#@click_config_file.configuration_option()
@click_config_file.configuration_option(implicit=True,provider=myprovider)
def cli():
    """ Show environment variables """
    logger.debug(f"Entering {os.path.basename(__file__)[:-3]}")

    for (key,value) in os.environ.items():
        if key!="PATH":
            click.echo(f"{key}:{value}")

if __name__ == '__main__':
    cli() # pylint: disable=no-value-for-parameter
