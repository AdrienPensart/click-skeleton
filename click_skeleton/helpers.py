'''Basic helpers used in many CLI'''
import logging
import datetime
import platform
import re
import string
import random
from collections import defaultdict
from typing import List, Any

logger = logging.getLogger(__name__)
true_values = ('enabled', 'y', 'yes', 't', 'true', 'True', 'on', '1')
false_values = ('', 'none', 'disabled', 'n', 'no', 'f', 'false', 'False', 'off', '0')


def recursive_str(data: Any) -> Any:
    '''Recursively convert multiple data type to string'''
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return [recursive_str(x) for x in data]
    if isinstance(data, dict):
        return {recursive_str(key): recursive_str(val) for key, val in data.items()}
    return str(data)


def str2bool(val: Any) -> bool:
    '''Converts any value to string and detects if it looks like a known bool value'''
    val = str(val).lower()
    if val in true_values:
        return True
    if val in false_values:
        return False
    raise ValueError(f"invalid truth value {val}")


def str_is_true(text: str) -> bool:
    '''Detects a known truthful string'''
    return str(text).lower() in true_values


def str_is_false(text: str) -> bool:
    '''Detects a known falsy string'''
    return str(text).lower() in false_values


def seconds_to_human(seconds: int) -> str:
    '''Human readable duration from seconds'''
    return str(datetime.timedelta(seconds=seconds))


def strip_colors(text: str) -> str:
    '''Remove all ANSI control characters'''
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def mysplit(text: str, delimiter: str = ',') -> List[str]:
    '''Split a string without returning empty list if string is empty'''
    return [x for x in text.split(delimiter) if x]


def raise_limits() -> bool:
    '''Permits to open a lot of system handles, supports Windows'''
    if platform.system() == 'Windows':
        logger.warning('Cannot raise system limits on Windows')
        return False
    # resource module is only available on UNIX systems
    import resource  # pylint: disable=import-error
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger.info(f"Current limits, soft and hard : {soft} {hard}")
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
        return True
    except (ValueError, OSError) as error:
        if 'macOS' in platform.platform():
            logger.info(f"Cannot raise system limits for current user on : {platform.platform()}")
        else:
            logger.critical(f'You may need to check ulimit parameter: {error}')
        return False


def random_password(size: int = 8) -> str:
    '''Generates a random string from size, composed of ascii letters and digits'''
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(size))


class PrettyDefaultDict(defaultdict):  # type: ignore
    '''Beautiful (correct printing) dict using collections.defaultdict'''
    __repr__ = dict.__repr__
