'''Simple example of a CLI made with click-skeleton'''
import logging
from typing import Any
import click
from click_skeleton import skeleton, sensible_context_settings, doc

PROG_NAME = 'example-cli'
__version__ = '1.0.0'
CONTEXT_SETTINGS = sensible_context_settings(PROG_NAME, __version__, auto_envvar_prefix='CLI')
logger = logging.getLogger(PROG_NAME)


@skeleton(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def main_cli(ctx: click.Context) -> Any:
    """Simple CLI example"""
    ctx.obj.config = 'global config storage'


@main_cli.command(short_help='Generates a README.rst', aliases=['doc'])
def readme() -> None:
    '''Uses gen_doc click-skeleton helper to generates a complete readme'''
    doc.gen_doc(main_cli, PROG_NAME, CONTEXT_SETTINGS)


@main_cli.command(short_help='Generates an exception')
def abort() -> None:
    '''Generates an exception on purpose (test)'''
    raise Exception('throw for test purposes')
