import pytest

from node import Node
from node import _absolute_path, _external_path
import conf


def test_absolute_path():
    assert _absolute_path('') == conf.META_DIR
    assert _absolute_path('/') == conf.META_DIR
    assert _absolute_path('foo/bar') == conf.META_DIR + '/foo/bar'
    assert _absolute_path('foo/bar/') == conf.META_DIR + '/foo/bar'
    with pytest.raises(RuntimeError):
        _absolute_path('../etc/hosts')


def test_external_path():
    assert _external_path(_absolute_path('')) == '/'
    assert _external_path(_absolute_path('/')) == '/'
    assert _external_path(_absolute_path('foo/bar')) == '/foo/bar'
    assert _external_path(_absolute_path('foo/bar/')) == '/foo/bar'
