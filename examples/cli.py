"""Simple example of a CLI made with click-skeleton"""
import logging
from typing import Any

import click

import examples.commands
from click_skeleton import ExpandedPath, add_options, backtrace, doc, skeleton

PROG_NAME = "example-cli"
__version__ = "1.0.0"
logger = logging.getLogger(PROG_NAME)

global_example_option = click.option("--global-example", help="A global option")
group_of_options = add_options(
    click.option("--option-one", help="First option"),
    click.option("--option-two", help="Second option"),
)


@skeleton(name=PROG_NAME, version=__version__, auto_envvar_prefix="CLI")
@click.pass_context
@global_example_option
@group_of_options
def main_cli(
    ctx: click.Context, global_example: str, option_one: str, option_two: str
) -> Any:
    """Simple CLI example"""
    backtrace.hook(strip_path=False, enable_on_envvar_only=False, on_tty=False)
    logger.info(f"in main_cli: ctx = {ctx}")
    logger.info(f"in main_cli: global_example = {global_example}")
    logger.info(f"in main_cli: option_one = {option_one}")
    logger.info(f"in main_cli: option_two = {option_two}")
    ctx.obj.global_option = global_example
    ctx.obj.config = "global config storage"


@main_cli.command(short_help="Generates a README.rst", aliases=["doc"])
@click.pass_context
@click.option(
    "--output",
    help="README output format",
    type=click.Choice(["rst", "markdown"]),
    default="rst",
    show_default=True,
)
def readme(ctx: click.Context, output: str) -> None:
    """Uses gen_doc click-skeleton helper to generates a complete readme"""
    doc.readme(main_cli, ctx.obj.prog_name, ctx.obj.context_settings, output)


@main_cli.command(short_help="Generates an exception")
@click.pass_context
def abort(ctx: click.Context) -> None:
    """Generates an exception on purpose (test)"""
    print(f"Global option = {ctx.obj.global_option}")
    print(f"One storage = {ctx.obj.config}")
    raise click.ClickException("throw for test purposes")


@main_cli.command(short_help="Expand option path")
@click.option(
    "--file", help="File path which expands", type=ExpandedPath(), default="~/plop"
)
def expanded_path(file: str) -> None:
    """Command with expanded path option"""
    print(file)


main_cli.add_groups_from_package(examples.commands)
