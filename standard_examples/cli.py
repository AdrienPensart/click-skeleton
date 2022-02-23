#!/usr/bin/env python3
'''A standard example without commands folder'''
import rich_click as click  # type: ignore

from click_skeleton import backtrace

backtrace.hook(strip_path=False, enable_on_envvar_only=False, on_tty=False)

CONTEXT_SETTINGS = {
    'max_content_width': 140,
    'terminal_width': 140,
    'help_option_names': ['-h', '--help'],
}


@click.group("example", context_settings=CONTEXT_SETTINGS)
def cli():
    """Simple CLI example"""
    click.echo("I'm a CLI")


@cli.command(help='a regular command')
def command():
    '''a long regular help of command'''
    click.echo("I'm a command")


@cli.command('raise', help='a command that raises an exception')
def _raise():
    '''a long regular help of command that raises an exception'''
    raise Exception("I'm an exception!")


@cli.group(help='I am a subgroup of commands')
def subgroup():
    '''a subgroup long help'''
    click.echo("I'm a subgroup")


@subgroup.command(help='I am a command in a subgroup')
def subcommand():
    '''a subcommand long help'''
    click.echo("I'm a subcommand")


if __name__ == '__main__':
    cli()
