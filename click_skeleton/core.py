'''Core features include an init function for skeleton'''
import logging
from typing import Optional, Dict, Any, Type
import attrdict  # type: ignore
import click
from click_help_colors import version_option  # type: ignore
from click_skeleton.advanced_group import RootAdvancedGroup
from click_skeleton.decorators import add_options

logger = logging.getLogger(__name__)


def sensible_context_settings(prog_name: str, version: str, **kwargs: Any) -> Dict[str, Any]:
    '''Prevents click from rewrapping help messages
    Set a global user storage for obj'''
    # obj = attrdict.AttrDict
    obj = attrdict.AttrDefault
    obj.prog_name = prog_name
    obj.version = version
    sensible_defaults = {
        'max_content_width': 140,
        'terminal_width': 140,
        'obj': obj,
        'help_option_names': ['-h', '--help']
    }
    sensible_defaults.update(kwargs)
    return sensible_defaults


def skeleton(
    context_settings: Optional[Dict[str, Any]] = None,
    cls: Optional[Type[click.Group]] = None,
) -> Any:
    '''Generates an AdvancedGroup with version options included'''

    if cls is None:
        cls = RootAdvancedGroup

    if context_settings is None:
        click.secho('Please provide a context_settings initializes with sensible_context_settings', fg='red', err=True)
        context_settings = sensible_context_settings(prog_name='unknown', version='unkown')

    prog_name = context_settings['obj'].prog_name
    version = context_settings['obj'].version
    return add_options(
        version_option(
            version,
            "--version", "-V",
            version_color='green',
            prog_name=prog_name,
            prog_name_color='yellow',
        ),
        click.group(
            context_settings=context_settings,
            cls=cls,
        ),
    )
