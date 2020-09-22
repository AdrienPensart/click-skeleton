'''Core features include an init function for skeleton'''
from typing import List, Dict, Any
import attrdict  # type: ignore
from click_help_colors import version_option  # type: ignore


def sensible_context_settings(prog_name: str, version: str, **kwargs: Any) -> Dict[str, Any]:
    '''Prevents click from rewrapping help messages
    Set a global user storage for obj'''
    obj = attrdict.AttrDict
    obj.prog_name = prog_name
    obj.version = version
    sensible_defaults = {
        'max_content_width': 140,
        'terminal_width': 140,
        'obj': attrdict.AttrDict,
        'help_option_names': ['-h', '--help']
    }
    sensible_defaults.update(kwargs)
    return sensible_defaults


def skeleton(context_settings: Dict[str, Any], **attrs: Any):  # type: ignore
    '''Generates an AdvancedGroup with version options included'''
    # avoid circular dependency
    from click_skeleton.version import version_cmd
    from click_skeleton.advanced_group import AdvancedGroup
    from click_skeleton.completion import completion_cli
    prog_name = context_settings['obj'].prog_name
    version = context_settings['obj'].version

    def wrapper(_: Any):  # type: ignore
        root_group = version_option(
            version,
            "--version", "-V",
            version_color='green',
            prog_name=prog_name,
            prog_name_color='yellow',
        )(AdvancedGroup(context_settings=context_settings, **attrs))
        root_group.add_command(completion_cli, 'completion')
        root_group.add_command(version_cmd, 'version')
        return root_group

    return wrapper


def add_options(options: List[Any]) -> Any:
    '''Helps to add options to command in the form of list'''
    def _add_options(func: Any) -> Any:
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options
