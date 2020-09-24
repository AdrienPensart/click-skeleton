'''Simple example of a CLI made with click-skeleton'''
import logging
from typing import Any
import click
from click_skeleton import add_options, skeleton, sensible_context_settings, doc

PROG_NAME = 'example-cli'
__version__ = '1.0.0'
CONTEXT_SETTINGS = sensible_context_settings(PROG_NAME, __version__, auto_envvar_prefix='CLI')
logger = logging.getLogger(PROG_NAME)

global_example_option = click.option('--global-example', help="A global option")
group_of_options = [
    click.option('--option-one', help="First option"),
    click.option('--option-two', help="Second option"),
]


@skeleton(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@add_options(global_example_option, group_of_options)
def main_cli(ctx: click.Context, global_example: str, option_one: str, option_two: str) -> Any:
    """Simple CLI example"""
    logger.info(f"in main_cli: ctx = {ctx}")
    logger.info(f"in main_cli: global_example = {global_example}")
    logger.info(f"in main_cli: option_one = {option_one}")
    logger.info(f"in main_cli: option_two = {option_two}")
    ctx.obj.global_option = global_example
    ctx.obj.config = 'global config storage'


@main_cli.command(short_help='Generates a README.rst', aliases=['doc'])
def readme() -> None:
    '''Uses gen_doc click-skeleton helper to generates a complete readme'''
    doc.gen_doc(main_cli, PROG_NAME, CONTEXT_SETTINGS)


@main_cli.command(short_help='Generates an exception')
@click.pass_context
def abort(ctx: click.Context) -> None:
    '''Generates an exception on purpose (test)'''
    print(f'Global option = {ctx.obj.global_option}')
    print(f'One storage = {ctx.obj.config}')
    raise Exception('throw for test purposes')
