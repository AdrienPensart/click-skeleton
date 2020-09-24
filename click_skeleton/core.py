'''Core features include an init function for skeleton'''
import logging
from typing import Optional, Any
import click
from box import Box  # type: ignore
from click_help_colors import version_option  # type: ignore
from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.decorators import add_options
from click_skeleton.version import version_cmd
from click_skeleton.completion import completion_cli

logger = logging.getLogger(__name__)


def skeleton(
    name: str,
    version: str,
    auto_envvar_prefix: Optional[str] = None,
    cls: Any = None,
    **kwargs: Any,
) -> Any:
    '''Generates an skeleton group with version options included'''
    auto_envvar_prefix = auto_envvar_prefix if auto_envvar_prefix is not None else name.upper()
    if cls is None:
        cls = AdvancedGroup

    sensible_context_settings = {
        'auto_envvar_prefix': auto_envvar_prefix,
        'max_content_width': 140,
        'terminal_width': 140,
        'help_option_names': ['-h', '--help'],
    }

    obj = Box(default_box=True)
    obj.prog_name = name
    obj.version = version
    obj.context_settings = sensible_context_settings

    context_settings = {
        'auto_envvar_prefix': auto_envvar_prefix,
        'max_content_width': 140,
        'terminal_width': 140,
        'obj': obj,
        'help_option_names': ['-h', '--help'],
    }

    commands = {
        'completion': completion_cli,
        'version': version_cmd,
    }
    return add_options(
        click.group(
            name=name,
            context_settings=context_settings,
            commands=commands,
            cls=cls,
            **kwargs,
        ),
        version_option(
            version,
            "--version", "-V",
            version_color='green',
            prog_name=name,
            prog_name_color='yellow',
        ),
    )
