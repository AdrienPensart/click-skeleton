'''Click skeleton helpers to ease CLI definitions'''
import os
import logging
import traceback
from typing import Any, Optional, Dict, List, Sequence
import colorama  # type: ignore
import click
import attrdict  # type: ignore
from click.testing import Result, CliRunner
from click_help_colors import HelpColorsGroup  # type: ignore
from click_didyoumean import DYMGroup  # type: ignore
from click_aliases import ClickAliasedGroup  # type: ignore

logger = logging.getLogger(__name__)
colorama.init(autoreset=True)


def sensible_context_settings(**kwargs: Any) -> Dict[str, Any]:
    '''Prevents click from rewrapping help messages
    Set a global user storage for obj'''
    sensible_defaults = {
        'max_content_width': 140,
        'terminal_width': 140,
        'obj': attrdict.AttrDict,
        'help_option_names': ['-h', '--help']
    }
    sensible_defaults.update(kwargs)
    return sensible_defaults


class ExpandedPath(click.ParamType):
    '''Re-implement click Path to auto-expand "~" on UNIX'''
    envvar_list_splitter = os.path.pathsep

    def __init__(
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Optional[str] = None,
    ):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = "file"
            self.path_type = "File"
        elif self.dir_okay and not self.file_okay:
            self.name = "directory"
            self.path_type = "Directory"
        else:
            self.name = "path"
            self.path_type = "Path"

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context]
    ) -> str:
        '''Expands user HOME and permits to check for write access without file needs to exist'''
        value = os.path.expanduser(value)
        is_dash = self.file_okay and self.allow_dash and value in (b"-", "-")
        if is_dash:
            return value

        if self.resolve_path:
            value = os.path.realpath(value)

        real_exists = os.path.exists(value)
        if self.exists and not real_exists:
            self.fail(f"{self.path_type} {value} does not exist.", param, ctx)

        if not self.file_okay and os.path.isfile(value):
            self.fail(f"{self.path_type} {value} is a file.", param, ctx)

        if not self.dir_okay and os.path.isdir(value):
            self.fail(f"{self.path_type} {value} is a directory.", param, ctx)

        if self.writable and not os.access(value, os.W_OK):
            pdir = os.path.dirname(value)
            if not pdir:
                pdir = '.'
            if not os.access(pdir, os.W_OK):
                self.fail(f"{self.path_type} {value} is not writable.", param, ctx)

        if self.readable and not os.access(value, os.R_OK):
            if not pdir:
                pdir = '.'
            if not os.access(pdir, os.R_OK):
                self.fail(f"{self.path_type} {value} is not readable.", param, ctx)

        return value


class AdvancedGroup(DYMGroup, ClickAliasedGroup, HelpColorsGroup):  # type: ignore
    '''Special click group with default plugins enabled :
    - did-you-mean
    - click aliases for commands
    - colored help message
    - auto help command
    '''
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs['help_headers_color'] = 'yellow'
        kwargs['help_options_color'] = 'green'
        super().__init__(*args, **kwargs)

        @click.command('help')
        @click.argument('command', nargs=-1)
        @click.pass_context
        def _help(ctx: Optional[click.Context], command: Sequence[click.Command]) -> None:
            '''Print help'''
            # we accept many commands, but only show help of the first one
            if not ctx:
                raise RuntimeError('no click context available')
            if command:
                first_command = command[0]
                command_obj = self.get_command(ctx, first_command)
                print(command_obj.get_help(ctx))
            else:
                if not ctx.parent:
                    raise RuntimeError('no click context parent available')
                print(ctx.parent.get_help())
        self.add_command(_help)


def add_options(options: List[Any]) -> Any:
    '''Helps to add options to command in the form of list'''
    def _add_options(func: Any) -> Any:
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def recursive_str(data: Any) -> Any:
    '''Recursively convert multiple data type to string'''
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return [recursive_str(x) for x in data]
    if isinstance(data, dict):
        return {recursive_str(key): recursive_str(val) for key, val in data.items()}
    return str(data)


def run_cli(cli_runner: CliRunner, called_cli: click.core.Group, *args: Any) -> str:
    '''Helper to run the CLI for pytest-click unit tests'''
    result: Result = cli_runner.invoke(called_cli, *args)
    logger.debug(result.output)
    if result.exception:
        exc_info = result.exc_info
        traceback.print_exception(*exc_info)  # type: ignore
    if result.exit_code != 0:
        elems = recursive_str(*args)
        elems = ' '.join(elems)
        logger.error(f'Failed : {cli_runner.get_default_prog_name(called_cli)} {elems}')
    assert result.exit_code == 0
    return result.output.rstrip()
