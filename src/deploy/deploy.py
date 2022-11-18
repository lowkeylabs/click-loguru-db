import click
from loguru import logger


if __name__ == 'src.deploy.deploy':
    from ..utils_init import *
else:
    from utils_init import *

@click.command()
@click.option('--env', '-e', default="dev", type=click.Choice(['dev', 'stg', 'prd'], case_sensitive=False), prompt='Enter env name to deploy', help='Env to deploy')
@click.option('--cloud', '-c', default="aws", type=click.Choice(['aws', 'gcp', 'azure'], case_sensitive=False), prompt='Enter cloud to deploy to', help='Cloud to deploy to')
@click_config_file.configuration_option(implicit=True,provider=myprovider)
def deploy(env, cloud):
    """ Command deploy docstring """
    logger.info("Entering command deploy")
    print(f'Deploying current application artifact to {env} environment in {cloud} cloud...')

if __name__ == '__main__':
    deploy()

