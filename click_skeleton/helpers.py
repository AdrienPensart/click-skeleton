import logging
import datetime
import platform
import re

logger = logging.getLogger(__name__)

true_values = ('enabled', 'y', 'yes', 't', 'true', 'True', 'on', '1')
false_values = ('disabled', 'n', 'no', 'f', 'false', 'False', 'off', '0')

def str2bool(val):
    val = str(val).lower()
    if val in true_values:
        return True
    if val in false_values:
        return 0
    raise ValueError(f"invalid truth value {val}")

def str_is_true(v):
    return str(v).lower() in true_values


def str_is_false(v):
    return str(v).lower() in false_values


def seconds_to_human(s) -> str:
    return str(datetime.timedelta(seconds=s))


def strip_colors(text) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def raise_limits() -> bool:
    if platform.system() == 'Windows':
        logger.debug('Cannot raise system limits on Windows')
        return False
    import resource  # pylint: disable=import-error
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger.info(f"Current limits, soft and hard : {soft} {hard}", soft, hard)
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
        return True
    except (ValueError, OSError) as e:
        logger.critical(f'You may need to check ulimit parameter: {e}')
        return False
