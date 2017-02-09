import os
import sys
import click
import traceback

CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX',
                        help_option_names=['-h', '--help'])

class Context(object):

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class TaxtoolCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('taxtool.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            traceback.print_exc()
            return
        return mod.cli


@click.command(cls=TaxtoolCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--home', type=click.Path(exists=True, file_okay=False,
                                        resolve_path=True),
              help='Changes the folder to operate on.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose, home):
    """A taxtool command line interface."""
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home