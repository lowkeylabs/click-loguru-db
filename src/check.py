import click
from loguru import logger

@click.command()
@click.option('--quick', is_flag=True, help='Perform checking function without module')
def check(quick):
    """ Command check docstring """
    logger.info("Entering command check")
    if quick:
        print(f'Quick form checking ...')
    else:
        print(f'Long form checking ...')

if __name__ == '__main__':
    check()

