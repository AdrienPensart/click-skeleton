"""Helpers tests"""

import pytest

from click_skeleton.helpers import raise_limits, random_password, str2bool


def test_str2bool() -> None:
    """Test that we are parsing bool string correctly"""
    assert str2bool("Y")
    assert not str2bool("N")
    with pytest.raises(Exception):
        str2bool("whatever")


def test_password() -> None:
    """Two random password has very high probability to be different"""
    assert random_password() != random_password()


def test_raise_limits() -> None:
    """Important helper as we may need a lot of file handles, does not work on Mac OS X"""
    assert raise_limits() is True
