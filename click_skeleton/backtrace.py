'''Replace default stacktrace printing with a beautiful one'''
import os
import sys
import traceback
from typing import Any, Union, List, Tuple, Optional
from types import TracebackType
import click


TRACEBACK_IDENTIFIER = 'Traceback (most recent call last):\n'


def _flush(message: str) -> None:
    '''Print message and flush stderr'''
    _ = sys.stderr.write(message + '\n')
    sys.stderr.flush()


class _Hook:
    '''Stacktrace hook'''
    def __init__(
            self,
            entries: Any,
            strip_path: bool = False,
    ):
        self.entries = entries
        self.strip = strip_path

    def reverse(self) -> None:
        '''Reverse stacktrace entries to ease reading'''
        self.entries = self.entries[::-1]

    def rebuild_entry(self, entry: Any) -> Any:
        '''Rebuild context of entry'''
        entry = list(entry)
        # This is the file path.
        entry[0] = os.path.basename(entry[0]) if self.strip else entry[0]
        # Always an int (entry line number)
        entry[1] = str(entry[1])

        new_entry = [
            click.style(f"{entry[1]}", fg="bright_red"),
            entry[0],
            click.style(f"{entry[2]}", fg="bright_green"),
            click.style(f"--> {entry[3]}", fg="bright_yellow"),
        ]

        return new_entry

    @staticmethod
    def align_all(entries: Any) -> List[int]:
        '''Align all stacktrace entries'''
        lengths = [0, 0, 0, 0]
        for entry in entries:
            for index, field in enumerate(entry):
                lengths[index] = max(lengths[index], len(str(field)))
        return lengths

    @staticmethod
    def align_entry(entry: Any, lengths: List[int]) -> str:
        '''Align one stacktrace entry'''
        return ' '.join(
            ['{0:{1}}'.format(field, lengths[index])  # pylint: disable=consider-using-f-string
             for index, field in enumerate(entry)]
        )

    def generate_backtrace(self) -> List[str]:
        '''Return the (potentially) aligned, rebuit traceback

        Yes, we iterate over the entries thrice. We sacrifice
        performance for code readability. I mean.. come on, how long can
        your traceback be that it matters?
        '''
        backtrace = []
        for entry in self.entries:
            backtrace.append(self.rebuild_entry(entry))

        # Get the lenght of the longest string for each field of an entry
        lengths = self.align_all(backtrace)
        return [self.align_entry(entry, lengths) for entry in backtrace]


def hook(
    strip_path: bool = False,
    enable_on_envvar_only: bool = False,
    on_tty: bool = False,
    trace: Optional[TracebackType] = None,
    tpe: Optional[type] = None,
    value: Optional[BaseException] = None,
) -> None:
    '''Hook'''
    if enable_on_envvar_only and 'ENABLE_BACKTRACE' not in os.environ:
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if on_tty and not isatty():
        return

    def backtrace_excepthook(
        tpe: Optional[Union[str, type]],
        value: Optional[BaseException],
        trace: Optional[TracebackType] = None,
    ) -> None:
        '''Don't know if we're getting traceback or traceback entries.
        We'll try to parse a traceback object.
        '''
        try:
            traceback_entries = traceback.extract_tb(trace)
            parser = _Hook(traceback_entries, strip_path)
        except AttributeError:
            parser = _Hook(trace, strip_path)

        if tpe is None:
            type_str = 'unknown'
        elif isinstance(tpe, str):
            type_str = tpe
        else:
            type_str = tpe.__name__

        tb_message = click.style('Traceback (Most recent call last):', fg="yellow")
        err_message = click.style(f"{type_str}: {value}", fg="bright_red")

        _flush(tb_message)
        backtrace = parser.generate_backtrace()
        backtrace.insert(len(backtrace), err_message)
        for entry in backtrace:
            _flush(entry)

    if trace:
        backtrace_excepthook(tpe=tpe, value=value, trace=trace)
    else:
        sys.excepthook = backtrace_excepthook


def unhook() -> None:
    '''Restore the default excepthook'''
    sys.excepthook = sys.__excepthook__  # type: ignore


def _extract_traceback(text: str) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    '''Receive a list of strings representing the input from stdin and return
    the restructured backtrace.

    This iterates over the output and once it identifies a hopefully genuine
    identifier, it will start parsing output.
    In the case the input includes a reraise (a Python 3 case), the primary
    traceback isn't handled, only the reraise.

    Each of the traceback lines are then handled two lines at a time for each
    stack object.

    Note that all parts of each stack object are stripped from newlines and
    spaces to keep the output clean.
    '''
    capture = False
    entries = []
    all_else = []
    ignore_trace = False

    # In python 3, a traceback may includes output from a reraise.
    # e.g, an exception is captured and reraised with another exception.
    # This marks that we should ignore
    if text.count(TRACEBACK_IDENTIFIER) == 2:
        ignore_trace = True

    location_info = False
    for line in text:
        if TRACEBACK_IDENTIFIER in line:
            if ignore_trace:
                ignore_trace = False
                continue
            capture = True
            location_info = True
        # We're not capturing and making sure we only read lines
        # with spaces since, after the initial identifier, all traceback lines
        # contain a prefix spacing.
        elif capture and line.startswith(' '):
            if location_info:
                # Line containing a file, line and module.
                line = line.strip()
                entries.append(line)
            else:
                # The corresponding line of source code.
                line = line.rstrip("\n")
                entries[-1] += ', ' + line
            location_info = not location_info
        elif capture:
            # Line containing the module call.
            entries.append(line)
            break
        else:
            # Add everything else before the traceback.
            all_else.append(line)

    traceback_entries = []
    # Build the traceback structure later passed for formatting.
    for _, line in enumerate(entries[:-2]):
        element = line.split(',', 3)
        _file = element[0].strip().lstrip('File').strip(' "')
        _line = element[1].strip().lstrip('line').strip()
        _in = element[2].strip().lstrip('in').strip()
        traceback_entries.append((_file, _line, _in))
    return traceback_entries, all_else
