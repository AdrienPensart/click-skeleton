'''Click skeleton helpers to ease CLI definitions'''
import logging

from click_skeleton.advanced_group import AdvancedGroup
from click_skeleton.core import skeleton
from click_skeleton.decorators import add_options
from click_skeleton.expanded_path import ExpandedPath

logger = logging.getLogger(__name__)

__all__ = [
    'AdvancedGroup',
    'ExpandedPath',
    'skeleton',
    'add_options',
]
