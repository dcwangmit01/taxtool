import click
from taxtool.cli import pass_context

@click.command('status', short_help='Just a placholder')
@pass_context
def cli(ctx):
    """Placehold description"""
    ctx.log('log example')
    ctx.vlog('vlog example')
