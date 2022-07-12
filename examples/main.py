#!/usr/bin/env python3
'''Main module, import commands and start CLI'''
import logging

from click_skeleton import helpers, version_checker
from examples.cli import PROG_NAME, __version__, main_cli

logger = logging.getLogger(__name__)


def main() -> None:
    '''click skeleton entrypoint, it will check if a new version is available'''
    helpers.raise_limits()
    version_check = version_checker.VersionCheckerThread(
        prog_name=PROG_NAME,
        current_version=__version__,
    )
    try:
        main_cli.main(prog_name=PROG_NAME, standalone_mode=False)
        version_check.print()
    except Exception as error:
        raise error


if __name__ == '__main__':
    main()
