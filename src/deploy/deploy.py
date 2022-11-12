import click

@click.command()
@click.option('--env', '-e', default="dev", type=click.Choice(['dev', 'stg', 'prd'], case_sensitive=False), prompt='Enter env name to deploy', help='Env to deploy')
@click.option('--cloud', '-c', default="aws", type=click.Choice(['aws', 'gcp', 'azure'], case_sensitive=False), prompt='Enter cloud to deploy to', help='Cloud to deploy to')
def deploy(env, cloud):
    print(f'Deploying current application artifact to {env} environment in {cloud} cloud...')

if __name__ == '__main__':
    deploy()

