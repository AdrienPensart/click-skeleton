'''Test example CLI'''
import logging
from typing import Any
import pytest
from click_skeleton.testing import run_cli
from click_skeleton.helpers import strip_colors
from examples.cli import main_cli, __version__

logger = logging.getLogger(__name__)


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_cli(cli_runner: Any) -> None:
    '''Test that CLI does not crash without any argument or options'''
    run_cli(cli_runner, main_cli)


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_cli_version(cli_runner: Any) -> None:
    '''Test that CLI version string is the same using all methods'''
    output1 = strip_colors(run_cli(cli_runner, main_cli, ['-V']))
    output2 = strip_colors(run_cli(cli_runner, main_cli, ['--version']))
    output3 = strip_colors(run_cli(cli_runner, main_cli, ['version']))
    assert output1 == output2 == output3
    assert __version__ in output1


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_cli_help(cli_runner: Any) -> None:
    '''Test that CLI help string is the same using all methods'''
    output1 = strip_colors(run_cli(cli_runner, main_cli, ['-h']))
    output2 = strip_colors(run_cli(cli_runner, main_cli, ['--help']))
    output3 = strip_colors(run_cli(cli_runner, main_cli, ['help']))
    assert output1 == output2 == output3


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_readme(cli_runner: Any) -> None:
    '''Test readme generation'''
    run_cli(cli_runner, main_cli, ["readme"])


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_completion_show(cli_runner: Any) -> None:
    '''Test generation of completion shell code'''
    run_cli(cli_runner, main_cli, ["completion", "show", "zsh"])


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_subgroup(cli_runner: Any) -> None:
    '''Test if subgroup is working'''
    run_cli(cli_runner, main_cli, ["subgroup"])


@pytest.mark.runner_setup(mix_stderr=False)  # type: ignore
def test_subcommand(cli_runner: Any) -> None:
    '''Test if subcommand is working'''
    run_cli(cli_runner, main_cli, ["subgroup", "subcommand"])
