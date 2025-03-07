"""Core features include an init function for skeleton"""

import logging
import re
from types import ModuleType
from typing import Any

import click
from click_help_colors.utils import _colorize
from dotmap import DotMap  # type: ignore

from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.decorators import add_options
from click_skeleton.defaults import DEFAULT_CONTEXT_SETTINGS
from click_skeleton.version import version_cmd

logger = logging.getLogger(__name__)


def version_option(
    version: None | str = None,
    prog_name: None | str = None,
    message: str = "%(prog)s, version %(version)s",
    message_color: None | str = None,
    prog_name_color: None | str = None,
    version_color: None | str = None,
    **kwargs: Any,
) -> Any:
    """Re-implement version handling with --version and -V shortcut"""
    msg_parts = []
    if prog_name is None:
        prog_name = ""
    if version is None:
        version = ""
    for placeholder in re.split(r"(%\(version\)s|%\(prog\)s)", message):
        if placeholder == "%(prog)s":
            msg_parts.append(_colorize(prog_name, prog_name_color or message_color))
        elif placeholder == "%(version)s":
            msg_parts.append(_colorize(version, version_color or message_color))
        else:
            msg_parts.append(_colorize(placeholder, message_color))
    message = "".join(msg_parts)

    return click.version_option(
        version, "--version", "-V", prog_name=prog_name, message=message, **kwargs
    )


def skeleton(
    name: str,
    version: str,
    auto_envvar_prefix: None | str = None,
    cls: Any = None,
    commands: None | dict[str, Any] = None,
    groups_package: None | ModuleType = None,
    **kwargs: Any,
) -> Any:
    """Generates an skeleton group with version options included"""
    auto_envvar_prefix = (
        auto_envvar_prefix if auto_envvar_prefix is not None else name.upper()
    )
    if cls is None:
        cls = AdvancedGroup

    sensible_context_settings = DEFAULT_CONTEXT_SETTINGS
    sensible_context_settings["auto_envvar_prefix"] = auto_envvar_prefix

    obj = DotMap()
    obj.prog_name = name
    obj.version = version
    obj.context_settings = sensible_context_settings

    context_settings = sensible_context_settings
    context_settings["auto_envvar_prefix"] = auto_envvar_prefix
    context_settings["obj"] = obj

    commands = commands if commands is not None else {}
    commands["version"] = version_cmd
    if groups_package is not None and cls is AdvancedGroup:
        kwargs["groups_package"] = groups_package

    return add_options(
        version_option(
            version=version,
            prog_name=name,
            version_color="green",
            prog_name_color="yellow",
        ),
        click.group(
            name=name,
            context_settings=context_settings,
            commands=commands,
            cls=cls,
            **kwargs,
        ),
    )
