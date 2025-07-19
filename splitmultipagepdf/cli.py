import click

from splitmultipagepdf.command.split_command import split_command

@click.group()
def cli():
    pass

cli.add_command(split_command)

def main():
    cli()

if __name__ == '__main__':
    main()