import logging
import datetime
import platform
import re
import string
import random
import collections
from typing import List, Any

logger = logging.getLogger(__name__)
true_values = ('enabled', 'y', 'yes', 't', 'true', 'True', 'on', '1')
false_values = ('disabled', 'n', 'no', 'f', 'false', 'False', 'off', '0')


def str2bool(val: Any) -> bool:
    val = str(val).lower()
    if val in true_values:
        return True
    if val in false_values:
        return False
    raise ValueError(f"invalid truth value {val}")


def str_is_true(v: str):
    return str(v).lower() in true_values


def str_is_false(v: str):
    return str(v).lower() in false_values


def seconds_to_human(s) -> str:
    return str(datetime.timedelta(seconds=s))


def strip_colors(text) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def mysplit(s: str, delim: str = ',') -> List[str]:
    if isinstance(s, list):
        return s
    if s is None:
        return []
    if isinstance(s, str):
        return [x for x in s.split(delim) if x]
    raise ValueError(s)


def raise_limits() -> bool:
    if platform.system() == 'Windows':
        logger.warning('Cannot raise system limits on Windows')
        return False
    import resource  # pylint: disable=import-error
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger.info(f"Current limits, soft and hard : {soft} {hard}")
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
        return True
    except (ValueError, OSError) as e:
        logger.critical(f'You may need to check ulimit parameter: {e}')
        return False


def random_password(size: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(size))


class PrettyDefaultDict(collections.defaultdict):
    __repr__ = dict.__repr__
