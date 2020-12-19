'''Generates shell code completion'''
import os
from typing import Optional
import click
import click_completion  # type: ignore
from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.decorators import add_options


completion_options = [
    click.option(
        '-i', '--case-insensitive',
        help="Case insensitive completion",
        is_flag=True,
    ),
    click.argument(
        'shell',
        required=False,
        type=click_completion.DocumentedChoice(click_completion.core.shells),
    ),
]

append_option = click.option(
    '--append/--overwrite',
    help="Append the completion code to the file",
    is_flag=True,
    default=None,
)


@click.group('completion', short_help="Shell completion", cls=AdvancedGroup)
def completion_cli() -> None:
    '''Shell completion subcommand'''


@completion_cli.command(short_help='Show the click-completion-command completion code', aliases=['print', 'generate'])
@add_options(completion_options)  # type: ignore
def show(shell: str, case_insensitive: bool) -> None:
    '''Generate shell code to enable completion'''
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))


@completion_cli.command(short_help='Install the click-completion-command completion')
@add_options(completion_options, append_option)  # type: ignore
@click.argument('path', required=False)
def install(append: bool, case_insensitive: bool, shell: str, path: Optional[str]) -> None:
    '''Auto install shell completion code in your rc file'''
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
    click.echo(f'{shell} completion installed in {path}')


def custom_startswith(string: str, incomplete: str) -> bool:
    '''A custom completion matching that supports case insensitive matching'''
    if os.environ.get('_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = custom_startswith
click_completion.init()
