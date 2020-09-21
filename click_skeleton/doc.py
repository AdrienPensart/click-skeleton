'''Generates a readme composed of all commands and subcommands help strings'''
from textwrap import indent
from typing import Dict, Any
import click
from . import AdvancedGroup


def gen_doc(
    main_cli: click.core.Group,
    prog_name: str,
    context_settings: Dict[str, Any]
) -> Any:
    '''Recursively output a beautiful readme on stdout, supports 3 levels of subcommands'''
    click.echo("Commands\n--------")
    click.echo(".. code-block::\n")
    base_ctx = click.Context(main_cli, info_name=prog_name, **context_settings)
    with base_ctx.scope():
        cli_help = main_cli.get_help(base_ctx)
        cli_help = indent(cli_help, '  ')
        click.echo(cli_help)
        for command_name, command in sorted(main_cli.commands.items()):
            if command.hidden:
                continue

            command_title = f"{prog_name} {command_name}"
            click.echo('\n')
            click.echo(command_title)
            click.echo('*' * len(command_title))
            click.echo(".. code-block::\n")

            command_ctx = click.Context(command, info_name=command_name, parent=base_ctx)
            with command_ctx.scope():
                command_help = command.get_help(command_ctx)
                command_help = indent(command_help, '  ')
                click.echo(command_help)

            if not isinstance(command, AdvancedGroup):
                continue

            for subcommand_name, subcommand in sorted(command.commands.items()):
                if subcommand_name == 'help' or subcommand.hidden:
                    continue

                subcommand_title = f"{prog_name} {command_name} {subcommand_name}"
                click.echo('\n')
                click.echo(subcommand_title)
                click.echo('*' * len(subcommand_title))
                click.echo(".. code-block::\n")
                subcommand_ctx = click.Context(subcommand, info_name=subcommand_name, parent=command_ctx)
                with subcommand_ctx.scope():
                    subcommand_help = subcommand.get_help(subcommand_ctx)
                    subcommand_help = indent(subcommand_help, '  ')
                    click.echo(subcommand_help)
