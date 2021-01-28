#!/usr/bin/env python3
import click

CONTEXT_SETTINGS = {
    'max_content_width': 140,
    'terminal_width': 140,
    'help_option_names': ['-h', '--help'],
}


@click.group("example", context_settings=CONTEXT_SETTINGS)
def cli():
    """Simple CLI example"""
    click.echo("I'm a CLI")


@cli.command()
def command():
    click.echo("I'm a command")


@cli.group()
def subgroup():
    click.echo("I'm a subgroup")


@subgroup.command()
def subcommand():
    click.echo("I'm a subcommand")


if __name__ == '__main__':
    # cli.main(prog_name="example")
    cli()
