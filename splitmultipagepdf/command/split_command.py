import click
from splitmultipagepdf.container.DefaultContainer import DefaultContainer
from splitmultipagepdf.service.split_service import SplitService

@click.command(
    name='split'
)
@click.argument('input_path')
@click.argument('output_path')
@click.option('--dpi', default=200, help='Resolution in DPI (default: 200)')
def split_command(input_path, output_path, dpi):
    default_container: DefaultContainer = DefaultContainer.getInstance()

    split_service: SplitService = default_container.get(SplitService)
    split_service.split(input_path=input_path, output_path=output_path, dpi=dpi)

