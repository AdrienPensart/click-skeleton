import asyncio
import time
import uvloop
import click
import logging
import string
import random
import os
import sys
import humanfriendly
from click_didyoumean import DYMGroup
from functools import wraps
from timeit import default_timer as timer
from .config import config

logger = logging.getLogger(__name__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def random_password(size=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(size))


class GroupWithHelp(DYMGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @click.command('help')
        @click.argument('command', nargs=-1)
        @click.pass_context
        def _help(ctx, command):
            '''Print help'''
            if command:
                argument = command[0]
                c = self.get_command(ctx, argument)
                print(c.get_help(ctx))
            else:
                print(ctx.parent.get_help())

        self.add_command(_help)


async def process(f, *args, **params):
    if asyncio.iscoroutinefunction(f):
        return await f(*args, **params)
    return f(*args, **params)


def timeit(f):
    @wraps(f)
    async def wrapper(*args, **params):
        start = time.time()
        result = await process(f, *args, **params)
        for_human = seconds_to_human(time.time() - start)
        if config.timings:
            logger.info('TIMINGS %s: %s', f.__name__, for_human)
        return result
    return wrapper


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def coro(f):
    f = asyncio.coroutine(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapper


def drier(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if config.dry:
            args = [str(a) for a in args] + ["%s=%s" % (k, v) for (k, v) in kwargs.items()]
            logger.info('DRY RUN: %s(%s)', f.__name__, ','.join(args))
            await asyncio.sleep(0)
        else:
            return await process(f, *args, **kwargs)
    return wrapper


def str2bool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise ValueError("invalid truth value %r" % (val,))


def bytes_to_human(b):
    return humanfriendly.format_size(b)


def seconds_to_human(s):
    import datetime
    return str(datetime.timedelta(seconds=s))


class Benchmark:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        logger.info("%s : %0.3g seconds", self.msg, t)
        self.time = t


class LazyProperty:
    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


def raise_limits():
    import resource
    try:
        _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger.info("Current limits, soft and hard : %s %s", _, hard)
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
        return True
    except Exception as e:
        logger.critical('You may need to check ulimit parameter: %s', e)
        return False


def restart():
    python = sys.executable
    print('Restarting myself: {} {}'.format(python, sys.argv))
    # only works on linux, not windows with WSL
    # os.execl(python, python, * sys.argv)
    # permit to exit from a thread
    os._exit(0)
