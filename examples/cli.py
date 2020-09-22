'''Simple example of a CLI made with click-skeleton'''
import logging
import click
from click_help_colors import version_option  # type: ignore
from click_skeleton import sensible_context_settings, AdvancedGroup, doc
from click_skeleton.completion import completion

PROG_NAME = 'simple-cli'
__version__ = '1.0.0'
CONTEXT_SETTINGS = sensible_context_settings(auto_envvar_prefix='CLI')
logger = logging.getLogger(PROG_NAME)


@click.group(
    PROG_NAME,
    cls=AdvancedGroup,
    context_settings=CONTEXT_SETTINGS,
)
@version_option(
    __version__,
    "--version", "-V",
    version_color='green',
    prog_name=PROG_NAME,
    prog_name_color='yellow',
)  # type: ignore
@click.pass_context
def main_cli(ctx: click.Context) -> None:
    """Simple CLI example"""
    ctx.obj.config = 'global config storage'


main_cli.add_command(completion, 'completion')


@main_cli.command('version', short_help='Print version')
def _version() -> None:
    '''Print version

       Equivalent : -V
    '''
    click.echo(f"{click.style(PROG_NAME, fg='yellow')}, version {click.style(__version__, fg='green')}")


@main_cli.command(short_help='Generates a README.rst', aliases=['doc'])
def readme() -> None:
    '''Uses gen_doc click-skeleton helper to generates a complete readme'''
    doc.gen_doc(main_cli, PROG_NAME, CONTEXT_SETTINGS)


@main_cli.command(short_help='Generates an exception')
def abort() -> None:
    '''Generates an exception on purpose (test)'''
    raise Exception('throw for test purposes')
