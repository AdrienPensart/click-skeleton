'''Import dynamically all modules in a directory'''
import os
import re
import sys
from typing import Iterator, Dict, Any, List


def import_all_modules(path: str, env: Dict[str, Any]) -> List[str]:
    """ Imports all modules residing directly in directory "path" into the provided environment
        (usually the callers environment). A typical call:
        importdir.do("example_dir", globals())
    """
    absolute_dirname = os.path.dirname(path)
    sys.path.append(absolute_dirname)
    modules = []
    for module_name in sorted(get_module_names_in_dir(absolute_dirname)):
        env[module_name] = __import__(module_name, env)
        if module_name != '__init__':
            modules.append(module_name)
    return modules


def get_module_names_in_dir(path: str) -> Iterator[str]:
    '''Returns a set of all module names residing directly in directory "path"'''
    # File name of a module:
    module_file_regexp = r"(.+)\.py(c?)$"
    # Looks for all python files in the directory (not recursively) and add their name to result:
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            regexp_result = re.search(module_file_regexp, entry)
            if regexp_result:
                yield regexp_result.group(1)
