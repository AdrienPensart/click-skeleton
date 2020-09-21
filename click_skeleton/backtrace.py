'''Replace default stacktrace printing with a beautiful one'''
import os
import sys
import traceback
from typing import Any, Dict, Union, List, Tuple, Optional
from types import TracebackType
from colorama import Fore, Style  # type: ignore


TRACEBACK_IDENTIFIER = 'Traceback (most recent call last):\n'
STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': Fore.RED + Style.BRIGHT + '{0}',
    'module': '{0}',
    'context': Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + '--> ' + Style.BRIGHT + '{0}',
}
CONVERVATIVE_STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': 'line ' + Fore.RED + Style.BRIGHT + '{0},',
    'module': 'File {0},',
    'context': 'in ' + Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + '--> ' + Style.BRIGHT + '{0}',
}


def _flush(message: str) -> None:
    '''Print message and flush stderr'''
    sys.stderr.write(message + '\n')
    sys.stderr.flush()


class _Hook:
    '''Stacktrace hook'''
    def __init__(self,
                 entries: Any,
                 align: bool = False,
                 strip_path: bool = False,
                 conservative: bool = False):
        self.entries = entries
        self.align = align
        self.strip = strip_path
        self.conservative = conservative

    def reverse(self) -> None:
        '''Reverse stacktrace entries to ease reading'''
        self.entries = self.entries[::-1]

    def rebuild_entry(self, entry: Any, styles: Dict[str, str]) -> Any:
        '''Rebuild context of entry'''
        entry = list(entry)
        # This is the file path.
        entry[0] = os.path.basename(entry[0]) if self.strip else entry[0]
        # Always an int (entry line number)
        entry[1] = str(entry[1])

        new_entry = [
            styles['line'].format(entry[1]) + Style.RESET_ALL,
            styles['module'].format(entry[0]) + Style.RESET_ALL,
            styles['context'].format(entry[2]) + Style.RESET_ALL,
            styles['call'].format(entry[3]) + Style.RESET_ALL
        ]
        if self.conservative:
            new_entry[0], new_entry[1] = new_entry[1], new_entry[0]

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
            ['{0:{1}}'.format(field, lengths[index])
             for index, field in enumerate(entry)]
        )

    def generate_backtrace(self, styles: Dict[str, str]) -> List[str]:
        '''Return the (potentially) aligned, rebuit traceback

        Yes, we iterate over the entries thrice. We sacrifice
        performance for code readability. I mean.. come on, how long can
        your traceback be that it matters?
        '''
        backtrace = []
        for entry in self.entries:
            backtrace.append(self.rebuild_entry(entry, styles))

        # Get the lenght of the longest string for each field of an entry
        lengths = self.align_all(backtrace) if self.align else [1, 1, 1, 1]
        return [self.align_entry(entry, lengths) for entry in backtrace]


def hook(
    reverse: bool = False,
    align: bool = False,
    strip_path: bool = False,
    enable_on_envvar_only: bool = False,
    on_tty: bool = False,
    conservative: bool = False,
    styles: Optional[Dict[str, str]] = None,
    trace: Optional[TracebackType] = None,
    tpe: Optional[type] = None,
    value: Optional[BaseException] = None,
) -> None:
    '''Hook the current excepthook to the backtrace.

    If `align` is True, all parts (line numbers, file names, etc..) will be
    aligned to the left according to the longest entry.

    If `strip_path` is True, only the file name will be shown, not its full
    path.

    If `enable_on_envvar_only` is True, only if the environment variable
    `ENABLE_BACKTRACE` is set, backtrace will be activated.

    If `on_tty` is True, backtrace will be activated only if you're running
    in a readl terminal (i.e. not piped, redirected, etc..).

    If `convervative` is True, the traceback will have more seemingly original
    style (There will be no alignment by default, 'File', 'line' and 'in'
    prefixes and will ignore any styling provided by the user.)

    See https://github.com/nir0s/backtrace/blob/master/README.md for
    information on `styles`.
    '''
    if enable_on_envvar_only and 'ENABLE_BACKTRACE' not in os.environ:
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if on_tty and not isatty():
        return

    chosen_styles: Dict[str, str]
    if conservative:
        chosen_styles = CONVERVATIVE_STYLES
        align = align or False
    elif styles:
        for key, default_value in STYLES.items():
            chosen_styles[key] = styles.get(key, default_value)
    else:
        chosen_styles = STYLES

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
            parser = _Hook(traceback_entries, align, strip_path, conservative)
        except AttributeError:
            parser = _Hook(trace, align, strip_path, conservative)

        if tpe is None:
            type_str = 'unknown'
        elif isinstance(tpe, str):
            type_str = tpe
        else:
            type_str = tpe.__name__

        tb_message = chosen_styles['backtrace'].format('Traceback ({0}):'.format(
            'Most recent call ' + ('first' if reverse else 'last'))) + \
            Style.RESET_ALL
        err_message = chosen_styles['error'].format(type_str + ': ' + str(value)) + \
            Style.RESET_ALL

        if reverse:
            parser.reverse()

        _flush(tb_message)
        backtrace = parser.generate_backtrace(chosen_styles)
        backtrace.insert(0 if reverse else len(backtrace), err_message)
        for entry in backtrace:
            _flush(entry)

    if trace:
        backtrace_excepthook(tpe=tpe, value=value, trace=trace)
    else:
        sys.excepthook = backtrace_excepthook


def unhook() -> None:
    '''Restore the default excepthook'''
    sys.excepthook = sys.__excepthook__


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
