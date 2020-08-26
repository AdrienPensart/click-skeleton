import click
import click_completion
from . import add_options, AdvancedGroup


completion_options = [
    click.option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion"),
    click.argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells)),
]

@click.group(help="Shell completion", cls=AdvancedGroup)
def completion():
    pass


@completion.command(help='Show the click-completion-command completion code')
@add_options(completion_options)
def show(shell, case_insensitive):
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))


@completion.command(help='Install the click-completion-command completion')
@click.option('--append/--overwrite', help="Append the completion code to the file", default=None)
@add_options(completion_options)
@click.argument('path', required=False)
def install(append, case_insensitive, shell, path):
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
    click.echo(f'{shell} completion installed in {path}')


def custom_startswith(string, incomplete):
    """A custom completion matching that supports case insensitive matching"""
    if os.environ.get('_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = custom_startswith
click_completion.init()
