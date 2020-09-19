#!/usr/bin/env python3
import click
from click_help_colors import version_option  # type: ignore
from click_skeleton import AdvancedGroup, backtrace, version_checker, doc
from click_skeleton.completion import completion
from click_skeleton.helpers import raise_limits

backtrace.hook(reverse=False, align=True, strip_path=False, enable_on_envvar_only=False, on_tty=False, conservative=False, styles={})
CONTEXT_SETTINGS = {
   'max_content_width': 140,
   'terminal_width': 140,
   'auto_envvar_prefix': 'MB',
   'help_option_names': ['-h', '--help']
}

prog_name = 'simple-cli'
__version__ = '1.0.0'

@click.group(
    prog_name,
    cls=AdvancedGroup,
    context_settings=CONTEXT_SETTINGS,
)
@version_option(
    __version__,
    "--version", "-V",
    version_color='green',
    prog_name=prog_name,
    prog_name_color='yellow',
)
def cli():
    """Simple CLI example"""

cli.add_command(completion, 'completion')

@cli.command('version', short_help='Print version')
def _version():
    '''Print version

       Equivalent : -V
    '''
    click.echo(f"{click.style(prog_name, fg='yellow')}, version {click.style(__version__, fg='green')}")


@cli.command(help='Generates a README.rst')
def readme():
    doc.gen_doc(cli, prog_name, CONTEXT_SETTINGS)


def main(**kwargs):
    version_check = version_checker.VersionCheckerThread(
        prog_name=prog_name,
        current_version=__version__,
    )
    try:
        return cli.main(prog_name=prog_name, **kwargs)
    finally:
        if version_check.is_alive():
            version_check.join()
            if version_check.new_version_warning:
                click.echo(version_check.new_version_warning, err=True)


if __name__ == '__main__':
    raise_limits()
    main()
