import click
from complex.cli import pass_context

@click.command('receipts', short_help='Process directories of receipts')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
@pass_context
def cli(ctx, path):
    """Turns a directory listing into a CSV"""
    if path is None:
        path = ctx.home
    ctx.log('Reading directory in %s', click.format_filename(path))
