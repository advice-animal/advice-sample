import click

@click.command()
@click.version_option()
def simple():
    pass

@click.command()
@click.version_option()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

@click.group()
@click.version_option()
def group():
    pass

if __name__ == '__main__':
    hello()
