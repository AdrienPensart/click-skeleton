'''Core features include an init function for skeleton'''
import re
import logging
from typing import Dict, Optional, Any
import click
from munch import Munch, DefaultFactoryMunch  # type: ignore
from click_help_colors.utils import _colorize  # type: ignore
from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.decorators import add_options
from click_skeleton.version import version_cmd
from click_skeleton.completion import completion_cli

logger = logging.getLogger(__name__)

DEFAULT_CONTEXT_SETTINGS = {
    'max_content_width': 140,
    'terminal_width': 140,
    'help_option_names': ['-h', '--help'],
}


def version_option(
        version: Optional[str] = None,
        prog_name: Optional[str] = None,
        message: str = "%(prog)s, version %(version)s",
        message_color: Optional[str] = None,
        prog_name_color: Optional[str] = None,
        version_color: Optional[str] = None,
        **kwargs: Any,
) -> Any:
    '''Re-implement version handling with --version and -V shortcut'''
    msg_parts = []
    for placeholder in re.split(r'(%\(version\)s|%\(prog\)s)', message):
        if placeholder == '%(prog)s':
            msg_parts.append(_colorize(prog_name, prog_name_color or message_color))
        elif placeholder == '%(version)s':
            msg_parts.append(_colorize(version, version_color or message_color))
        else:
            msg_parts.append(_colorize(placeholder, message_color))
    message = ''.join(msg_parts)

    return click.version_option(
        version,
        '--version', '-V',
        prog_name=prog_name,
        message=message,
        **kwargs
    )


def skeleton(
    name: str,
    version: str,
    auto_envvar_prefix: Optional[str] = None,
    cls: Any = None,
    commands: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Any:
    '''Generates an skeleton group with version options included'''
    auto_envvar_prefix = auto_envvar_prefix if auto_envvar_prefix is not None else name.upper()
    if cls is None:
        cls = AdvancedGroup

    sensible_context_settings = DEFAULT_CONTEXT_SETTINGS
    sensible_context_settings['auto_envvar_prefix'] = auto_envvar_prefix

    obj = DefaultFactoryMunch(Munch)
    obj.prog_name = name
    obj.version = version
    obj.context_settings = sensible_context_settings

    context_settings = sensible_context_settings
    context_settings['auto_envvar_prefix'] = auto_envvar_prefix
    context_settings['obj'] = obj

    commands = commands if commands is not None else {}
    commands['completion'] = completion_cli
    commands['version'] = version_cmd
    return add_options(
        version_option(
            version=version,
            prog_name=name,
            version_color='green',
            prog_name_color='yellow',
        ),
        click.group(
            name=name,
            context_settings=context_settings,
            commands=commands,
            cls=cls,
            **kwargs,
        ),
    )
