import click
from app.cli import pass_context


@click.command('status', short_help='Just a placholder')
@pass_context
def cli(ctx):
    """Placehold description"""
    ctx.log('log example')
    ctx.vlog('vlog example')
