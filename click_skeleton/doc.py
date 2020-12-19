'''Generates a readme composed of all commands and subcommands help strings'''
from textwrap import indent
from typing import Dict, Any
import click
from . import AdvancedGroup


def write_header(text: str, char: str) -> None:
    '''Write line followed by a newline containing as many chars'''
    click.echo("\n" + text)
    click.echo(char * len(text))


def write_codeblock(code: str, output: str) -> None:
    '''Write a console codeblock, either in rst or markdown'''
    if output == 'rst':
        indented_code = indent(code, '  ')
        click.echo(".. code-block::\n")
        click.echo(indented_code)
    elif output == 'markdown':
        click.echo('```')
        click.echo(code)
        click.echo('```')


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

    base_ctx = click.Context(main_cli, info_name=prog_name, **context_settings)
    with base_ctx.scope():
        cli_help = main_cli.get_help(base_ctx)
        write_codeblock(cli_help, output)

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
                command_help = command.get_help(command_ctx)
                write_codeblock(command_help, output)

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
                    subcommand_help = subcommand.get_help(subcommand_ctx)
                    write_codeblock(subcommand_help, output)
