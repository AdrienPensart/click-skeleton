#!/usr/bin/env python3
'''Simple example of a CLI made with click-skeleton'''
from typing import Any
import click
from click_help_colors import version_option  # type: ignore
from click_skeleton import sensible_context_settings, AdvancedGroup, backtrace, version_checker, doc
from click_skeleton.completion import completion
from click_skeleton.helpers import raise_limits

backtrace.hook(reverse=False, align=True, strip_path=False, enable_on_envvar_only=False, on_tty=False, conservative=False, styles={})

PROG_NAME = 'simple-cli'
__version__ = '1.0.0'
CONTEXT_SETTINGS = sensible_context_settings(auto_envvar_prefix='CLI')


@click.group(
    PROG_NAME,
    cls=AdvancedGroup,
    context_settings=CONTEXT_SETTINGS,
)
@version_option(
    __version__,
    "--version", "-V",
    version_color='green',
    prog_name=PROG_NAME,
    prog_name_color='yellow',
)  # type: ignore
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Simple CLI example"""
    ctx.obj.config = 'global config storage'


cli.add_command(completion, 'completion')


@cli.command('version', short_help='Print version')
def _version() -> None:
    '''Print version

       Equivalent : -V
    '''
    click.echo(f"{click.style(PROG_NAME, fg='yellow')}, version {click.style(__version__, fg='green')}")


@cli.command(short_help='Generates a README.rst', aliases=['doc'])
def readme() -> None:
    '''Uses gen_doc click-skeleton helper to generates a complete readme'''
    doc.gen_doc(cli, PROG_NAME, CONTEXT_SETTINGS)


@cli.command(short_help='Generates an exception')
def abort() -> None:
    '''Generates an exception on purpose (test)'''
    raise Exception('throw for test purposes')


def main(**kwargs: Any) -> int:
    '''click skeleton entrypoint, it will check if a new version is available'''
    version_check = version_checker.VersionCheckerThread(
        prog_name=PROG_NAME,
        current_version=__version__,
    )
    try:
        exit_code = int(cli.main(prog_name=PROG_NAME, **kwargs))
        version_check.print()
        return exit_code
    except Exception as error:
        raise error


if __name__ == '__main__':
    raise_limits()
    main()
