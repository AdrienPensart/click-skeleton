import pytest
from click_skeleton.helpers import str2bool

def test_str2bool():
    assert str2bool('Y')
    assert not str2bool('N')
    with pytest.raises(Exception):
        str2bool('whatever')
