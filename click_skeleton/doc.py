'''Generates a readme composed of all commands and subcommands help strings'''
from textwrap import indent
from typing import Any, Dict

import click
from rich_click import RichCommand  # type: ignore

from click_skeleton.advanced_group import AdvancedGroup


def write_header(text: str, char: str) -> None:
    '''Write line followed by a newline containing as many chars'''
    click.echo("\n" + text)
    click.echo(char * len(text))


def codeblock(code: str, output: str) -> None:
    '''Write a codeblock'''
    try:
        if output == 'rst':
            click.echo(".. code-block::\n")
            code = indent(code, '  ')
        elif output == 'markdown':
            click.echo('''```''')
        print(code)
    finally:
        if output == 'markdown':
            click.echo('''```''')


def readme(
    main_cli: click.core.Group,
    prog_name: str,
    context_settings: Dict[str, Any],
    output: str = 'rst',
) -> Any:
    '''Recursively output a beautiful readme on stdout, supports 3 levels of subcommands'''
    if output == 'rst':
        write_header("Commands", '-')
    elif output == 'markdown':
        click.echo('# Commands\n')

    AdvancedGroup.format_help = click.Group.format_help
    RichCommand.format_help = click.Command.format_help

    base_ctx = click.Context(main_cli, info_name=prog_name, **context_settings)
    with base_ctx.scope():
        codeblock(main_cli.get_help(base_ctx), output)

        for command_name, command in sorted(main_cli.commands.items()):
            if command.hidden:
                continue

            command_header = f"{prog_name} {command_name}"
            if output == 'rst':
                write_header(command_header, '*')
            elif output == 'markdown':
                click.echo(f'\n## {command_header}\n')

            command_ctx = click.Context(command, info_name=command_name, parent=base_ctx)
            with command_ctx.scope():
                codeblock(command.get_help(command_ctx), output)

            if not isinstance(command, AdvancedGroup):
                continue

            for subcommand_name, subcommand in sorted(command.commands.items()):
                if subcommand_name == 'help' or subcommand.hidden:
                    continue

                subcommand_header = f"{prog_name} {command_name} {subcommand_name}"
                if output == 'rst':
                    write_header(f"{subcommand_header}", '*')
                elif output == 'markdown':
                    click.echo(f'\n### {subcommand_header}\n')

                subcommand_ctx = click.Context(subcommand, info_name=subcommand_name, parent=command_ctx)
                with subcommand_ctx.scope():
                    codeblock(subcommand.get_help(subcommand_ctx), output)
