#!/usr/bin/env python3
'''Main module, import commands and start CLI'''
import sys
import logging
from typing import Any
from click_skeleton import helpers, backtrace, version_checker
from examples.cli import main_cli, PROG_NAME, __version__

logger = logging.getLogger(__name__)

backtrace.hook(
    reverse=False,
    align=True,
    strip_path=False,
    enable_on_envvar_only=False,
    on_tty=False,
    conservative=False,
)


def main(**kwargs: Any) -> int:
    '''click skeleton entrypoint, it will check if a new version is available'''
    helpers.raise_limits()
    version_check = version_checker.VersionCheckerThread(
        prog_name=PROG_NAME,
        current_version=__version__,
    )
    try:
        exit_code = int(main_cli.main(prog_name=PROG_NAME, **kwargs))
        version_check.print()
        return exit_code
    except Exception as error:
        raise error


if __name__ == '__main__':
    sys.exit(main())
