'''Improved click.testing test runner'''
import logging
import traceback
from typing import Any
import click
from click.testing import Result, CliRunner
from click_skeleton import helpers

logger = logging.getLogger(__name__)


def run_cli(cli_runner: CliRunner, called_cli: click.core.Group, *args: Any) -> str:
    '''Helper to run the CLI for pytest-click unit tests'''
    result: Result = cli_runner.invoke(called_cli, *args)
    logger.debug(result.output)
    if result.exception:
        exc_info = result.exc_info
        traceback.print_exception(*exc_info)  # type: ignore
    if result.exit_code != 0:
        elems = helpers.recursive_str(*args)
        elems = ' '.join(elems)
        logger.error(f'Failed : {cli_runner.get_default_prog_name(called_cli)} {elems}')
    assert result.exit_code == 0
    return result.output.rstrip()
