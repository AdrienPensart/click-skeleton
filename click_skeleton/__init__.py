'''Click skeleton helpers to ease CLI definitions'''
import logging
import colorama  # type: ignore
import click
from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.expanded_path import ExpandedPath
from click_skeleton.core import skeleton
from click_skeleton.decorators import add_options

logger = logging.getLogger(__name__)

# enable colors by default
colorama.init(autoreset=True)

# little hacky but prevent click from rewraping
click.formatting.HelpFormatter.write_dl.__defaults__ = (50, 2)  # type: ignore

__all__ = [
    'AdvancedGroup',
    'ExpandedPath',
    'skeleton',
    'add_options',
]
