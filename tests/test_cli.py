# pylint: disable=missing-module-docstring,missing-function-docstring
import logging
from typing import Any

import pytest
from beartype import beartype

from click_skeleton.helpers import strip_colors
from click_skeleton.testing import run_cli
from examples.cli import __version__, main_cli

logger = logging.getLogger(__name__)


@beartype
def test_cli(cli_runner: Any) -> None:
    run_cli(cli_runner, main_cli)


@beartype
def test_version(cli_runner: Any) -> None:
    output1 = strip_colors(run_cli(cli_runner, main_cli, ["-V"]))
    output2 = strip_colors(run_cli(cli_runner, main_cli, ["--version"]))
    output3 = strip_colors(run_cli(cli_runner, main_cli, ["version"]))
    assert output1 == output2 == output3
    assert __version__ in output1


@beartype
def test_help(cli_runner: Any) -> None:
    output1 = strip_colors(run_cli(cli_runner, main_cli, ["-h"]))
    output2 = strip_colors(run_cli(cli_runner, main_cli, ["--help"]))
    output3 = strip_colors(run_cli(cli_runner, main_cli, ["help"]))
    assert output1 == output2 == output3


@beartype
def test_subcommand_help(cli_runner: Any) -> None:
    output1 = strip_colors(run_cli(cli_runner, main_cli, ["subgroup", "-h"]))
    output2 = strip_colors(run_cli(cli_runner, main_cli, ["subgroup", "--help"]))
    output3 = strip_colors(run_cli(cli_runner, main_cli, ["subgroup", "help"]))
    assert output1 == output2 == output3


@beartype
def test_subcommand_raise(cli_runner: Any) -> None:
    with pytest.raises(Exception):
        run_cli(cli_runner, main_cli, ["abort"])


@beartype
def test_subcommand_expanded_path(cli_runner: Any) -> None:
    run_cli(cli_runner, main_cli, ["expanded-path"])


@beartype
def test_readme_rst(cli_runner: Any) -> None:
    run_cli(cli_runner, main_cli, ["readme", "--output", "rst"])


@beartype
def test_readme_markdown(cli_runner: Any) -> None:
    run_cli(cli_runner, main_cli, ["readme", "--output", "markdown"])


@beartype
def test_subgroup(cli_runner: Any) -> None:
    run_cli(cli_runner, main_cli, ["subgroup"])


@beartype
def test_subcommand(cli_runner: Any) -> None:
    run_cli(
        cli_runner,
        main_cli,
        [
            "subgroup",
            "subcommand",
            "--myoptions",
            "plop1,plop2",
            "--myoptions",
            "plop3",
        ],
    )
