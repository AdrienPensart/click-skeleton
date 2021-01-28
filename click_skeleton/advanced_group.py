'''Advanced group is a colored, what-did-you-mean with aliases commands group'''
import logging
import pkgutil
import sys
import importlib
from types import ModuleType
from typing import Any, Optional
import click
from click_help_colors import HelpColorsGroup  # type: ignore
from click_didyoumean import DYMGroup  # type: ignore
from click_aliases import ClickAliasedGroup  # type: ignore
from click_skeleton.exceptions import AlreadyRegistered

logger = logging.getLogger(__name__)


class AdvancedGroup(ClickAliasedGroup, DYMGroup, HelpColorsGroup):  # type: ignore
    '''Special click group with default plugins enabled :
    - did-you-mean
    - click aliases for commands
    - colored help message
    - auto help command
    '''
    def __init__(self, *args: Any, aliases: Optional[str] = None, **kwargs: Any):
        kwargs['help_headers_color'] = 'yellow'
        kwargs['help_options_color'] = 'green'
        super().__init__(*args, **kwargs)
        self.aliases = aliases if aliases is not None else []

        @click.command('help')
        @click.pass_context
        def _help(ctx: Optional[click.Context]) -> None:
            '''Print help'''
            # we accept many commands, but only show help of the first one
            if not ctx:
                raise RuntimeError('no click context available')
            if not ctx.parent:
                raise RuntimeError('no click context parent available')
            click.echo(ctx.parent.get_help(), color=ctx.color)
            ctx.exit()

        self.add_command(_help, 'help')

    def add_group(self, cmd: "AdvancedGroup", name: str) -> None:
        """Registers another :class:`Group` with this group.  If the name
        is not provided, the name of the group is used.
        """
        self.add_command(cmd, name)

        if not cmd.aliases:
            return

        if name in self._commands:
            raise AlreadyRegistered(f'{name} group is already registered')

        self._commands[name] = cmd.aliases
        for alias in cmd.aliases:
            if alias in self._aliases:
                raise AlreadyRegistered(f'Alias {alias} is already used by {self._aliases[alias]}')
            self._aliases[alias] = name

    def add_groups_from_package(self, package: ModuleType) -> None:
        '''loads commands dynamically, not supported by pyinstaller'''
        package_name = package.__name__
        package = sys.modules[package_name]
        modules_by_name = {
            name: importlib.import_module(package_name + '.' + name)
            for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)  # type: ignore
        }
        for module_name, module in modules_by_name.items():
            try:
                cli = getattr(module, 'cli')
                if cli.name != 'cli':
                    self.add_group(cli, cli.name)
                else:
                    self.add_group(cli, module_name)
            except AttributeError:
                click.secho(f'''Command module {module_name} does not contain a 'cli' definition''', fg='red', err=True)
