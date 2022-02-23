'''Core features include an init function for skeleton'''
import logging
import re
from typing import Any, Dict, Optional

import rich_click as click  # type: ignore
from munch import DefaultFactoryMunch, Munch  # type: ignore

from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.completion import completion_cli
from click_skeleton.decorators import add_options
from click_skeleton.defaults import DEFAULT_CONTEXT_SETTINGS
from click_skeleton.version import version_cmd

logger = logging.getLogger(__name__)

click.rich_click.SHOW_ARGUMENTS = True


def version_option(
        version: Optional[str] = None,
        prog_name: Optional[str] = None,
        message: str = "%(prog)s, version %(version)s",
        **kwargs: Any,
) -> Any:
    '''Re-implement version handling with --version and -V shortcut'''
    msg_parts = []
    for placeholder in re.split(r'(%\(version\)s|%\(prog\)s)', message):
        if placeholder == '%(prog)s':
            msg_parts.append(click.style(prog_name, fg='yellow'))
        elif placeholder == '%(version)s':
            msg_parts.append(click.style(version, fg='green'))
        else:
            msg_parts.append(placeholder)
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
        ),
        click.group(
            name=name,
            context_settings=context_settings,
            commands=commands,
            cls=cls,
            **kwargs,
        ),
    )
