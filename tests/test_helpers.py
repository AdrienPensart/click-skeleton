import pytest
from click_skeleton.helpers import str2bool, random_password, raise_limits


def test_str2bool():
    assert str2bool('Y')
    assert not str2bool('N')
    with pytest.raises(Exception):
        str2bool('whatever')


def test_password():
    assert random_password() != random_password()


def test_raise_limits():
    assert raise_limits() is True
