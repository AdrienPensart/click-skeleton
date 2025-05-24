"""A subgroup example"""

import click

from click_skeleton import AdvancedGroup
from click_skeleton.helpers import split_arguments


@click.group(
    short_help="A sub group",
    cls=AdvancedGroup,
    aliases=["subgroup-alias"],
    invoke_without_command=True,
)
def cli() -> None:
    """I am a subgroup!"""


@cli.command(short_help="A sub command")
@click.option(
    "--myoptions",
    help="A splitted option",
    multiple=True,
    callback=split_arguments,
)
def subcommand(myoptions: list[str]) -> None:
    """I am a subcommand!"""
    print(f"hello from subcommand! {myoptions}")
