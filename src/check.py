import click

@click.command()
@click.option('--quick', is_flag=True, help='Perform checking function without module')
def check(quick):
    if quick:
        print(f'Quick form checking ...')
    else:
        print(f'Long form checking ...')

if __name__ == '__main__':
    check()

