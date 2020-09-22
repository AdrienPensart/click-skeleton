'''Advanced group is a colored, what-did-you-mean with aliases commands group'''
import logging
from typing import Any, Optional, Sequence
import click
from click_help_colors import HelpColorsGroup  # type: ignore
from click_didyoumean import DYMGroup  # type: ignore
from click_aliases import ClickAliasedGroup  # type: ignore

logger = logging.getLogger(__name__)


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
        self.add_command(_help, 'help')


class RootAdvancedGroup(AdvancedGroup):
    '''Group to use for root main CLI, include completion and version commands'''
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # avoid circular dependencies
        from click_skeleton.version import version_cmd
        from click_skeleton.completion import completion_cli
        self.add_command(completion_cli, 'completion')
        self.add_command(version_cmd, 'version')
