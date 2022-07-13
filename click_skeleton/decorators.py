'''Decorators and helpers to add options to groups and commands, and compose decorators'''
from typing import Union, Any, Iterable, Optional
import click


def flatten(iterables: Union[Any, Iterable[Any]]) -> Iterable[Any]:
    '''Recursively flatten argument'''
    for element in iterables:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            yield from flatten(element)
        else:
            yield element


def add_options(*options: Any) -> Any:
    '''Helps to add options to command in the form of list'''
    def _add_options(func: Any) -> Any:
        for option in reversed(list(flatten(options))):
            func = option(func)
        return func
    return _add_options


def group(name: Optional[str] = None, **attrs: Any) -> Any:
    """Creates a new :class:`Group` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Group`.
    """
    from click_skeleton.advanced_group import AdvancedGroup
    attrs.setdefault("cls", AdvancedGroup)
    return click.command(name, **attrs)
