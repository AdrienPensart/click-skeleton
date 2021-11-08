'''Helpers tests'''
import platform
import pytest
from click_skeleton.helpers import str2bool, random_password, raise_limits


def test_str2bool() -> None:
    '''Test that we are parsing bool string correctly'''
    assert str2bool('Y')
    assert not str2bool('N')
    with pytest.raises(Exception):
        str2bool('whatever')


def test_password() -> None:
    '''Two random password has very high probability to be different'''
    assert random_password() != random_password()


def test_raise_limits() -> None:
    '''Important helper as we may need a lot of file handles, does not work on Mac OS X'''
    if platform.system() in ('Darwin', 'Windows'):
        assert raise_limits() is False
    else:
        assert raise_limits() is True
