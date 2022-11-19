import click
from loguru import logger


if __name__ == 'src.build.build':
    from ..utils_init import *
else:
    from utils_init import *

@click.command()
@click.option('--docker', is_flag=True, help='Indicates the project should be built into docker image')
@click_config_file.configuration_option()
def build(docker):
    """ Command build docstring"""
    logger.info("Entering command build")
    if docker:
        print(f'Building this repo into a docker image...')
    else:
        print(f'Building this repo using default method...')

if __name__ == '__main__':
    build()

