'''ExpandedPath is a improved click.Path with HOME expanded and check for write access'''
import logging
import os
from typing import Optional
import click

logger = logging.getLogger(__name__)


class ExpandedPath(click.ParamType):
    '''Re-implement click Path to auto-expand "~" on UNIX'''
    envvar_list_splitter = os.path.pathsep

    def __init__(
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        path_type: Optional[str] = None,
    ):
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.type = path_type

        if self.file_okay and not self.dir_okay:
            self.name = "file"
            self.path_type = "File"
        elif self.dir_okay and not self.file_okay:
            self.name = "directory"
            self.path_type = "Directory"
        else:
            self.name = "path"
            self.path_type = "Path"

    def convert(
        self,
        value: str,
        param: Optional[click.Parameter],
        ctx: Optional[click.Context]
    ) -> str:
        '''Expands user HOME and permits to check for write access without file needs to exist'''
        value = os.path.expanduser(value)
        is_dash = self.file_okay and self.allow_dash and value in (b"-", "-")
        if is_dash:
            return value

        if self.resolve_path:
            value = os.path.realpath(value)

        real_exists = os.path.exists(value)
        if self.exists and not real_exists:
            self.fail(f"{self.path_type} {value} does not exist.", param, ctx)

        if not self.file_okay and os.path.isfile(value):
            self.fail(f"{self.path_type} {value} is a file.", param, ctx)

        if not self.dir_okay and os.path.isdir(value):
            self.fail(f"{self.path_type} {value} is a directory.", param, ctx)

        if self.writable and not os.access(value, os.W_OK):
            pdir = os.path.dirname(value)
            if not pdir:
                pdir = '.'
            if not os.access(pdir, os.W_OK):
                self.fail(f"{self.path_type} {value} is not writable.", param, ctx)

        if self.readable and not os.access(value, os.R_OK):
            pdir = os.path.dirname(value)
            if not pdir:
                pdir = '.'
            if not os.access(pdir, os.R_OK):
                self.fail(f"{self.path_type} {value} is not readable.", param, ctx)

        return value
