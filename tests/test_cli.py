'''Test example CLI'''
import logging
import pytest
from click_skeleton import run_cli
from click_skeleton.helpers import strip_colors
from examples.cli import cli, __version__

logger = logging.getLogger(__name__)


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli(cli_runner) -> None:
    '''Test that CLI does not crash without any argument or options'''
    run_cli(cli_runner, cli)


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_version(cli_runner) -> None:
    '''Test that CLI version string is the same using all methods'''
    output1 = strip_colors(run_cli(cli_runner, cli, ['-V']))
    output2 = strip_colors(run_cli(cli_runner, cli, ['--version']))
    output3 = strip_colors(run_cli(cli_runner, cli, ['version']))
    assert output1 == output2 == output3
    assert __version__ in output1


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_help(cli_runner) -> None:
    '''Test that CLI help string is the same using all methods'''
    output1 = strip_colors(run_cli(cli_runner, cli, ['-h']))
    output2 = strip_colors(run_cli(cli_runner, cli, ['--help']))
    output3 = strip_colors(run_cli(cli_runner, cli, ['help']))
    assert output1 == output2 == output3


@pytest.mark.runner_setup(mix_stderr=False)
def test_readme(cli_runner) -> None:
    '''Test readme generation'''
    run_cli(cli_runner, cli, ["readme"])


@pytest.mark.runner_setup(mix_stderr=False)
def test_completion_show(cli_runner) -> None:
    '''Test generation of completion shell code'''
    run_cli(cli_runner, cli, ["completion", "show", "zsh"])
