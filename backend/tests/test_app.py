import os

import pytest
from starlette.testclient import TestClient

import app
from ._utils import filesystem


EXISTED_DIR = 'existed-dir'
EXISTED_FILE = os.path.join(EXISTED_DIR, 'existed-file')
NOT_EXISTED_DIR = 'not-existed-dir'
NOT_EXISTED_FILE = os.path.join(EXISTED_DIR, 'not-existed-file')

EXISTED_FILE_CONTENT = b'EXISTED_FILE_CONTENT'
NEW_CONTENT = b'NEW_CONTENT'


@pytest.fixture
def client():
    return TestClient(app.app)


@pytest.fixture
def authed():
    orig_get_user = app.get_user
    app.get_user = lambda *args, **kwargs: {'username': 'fans656'}
    yield
    app.get_user = orig_get_user


def test_index_should_return_html(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.headers['content-type'].startswith('text/html')


def test_unauthed(client):
    # upload require auth
    assert client.post('/api/file/').status_code == 401
    assert client.post('/api/file/' + EXISTED_DIR).status_code == 401
    assert client.post('/api/file/' + NOT_EXISTED_DIR).status_code == 401
    assert client.post('/api/file/' + EXISTED_FILE).status_code == 401
    assert client.post('/api/file/' + NOT_EXISTED_FILE).status_code == 401


def test_upload(client, authed, filesystem):
    # directory can not be target path
    assert client.post('/api/file/').status_code == 400
    # upload to root
    path = '/api/file/test.txt'
    assert client.post(path, data=NEW_CONTENT).status_code == 200
    assert client.get(path).content == NEW_CONTENT
    # upload to nested folder
    path = '/api/file/foo/bar'
    assert client.post(path, data=NEW_CONTENT).status_code == 200
    assert client.get(path).content == NEW_CONTENT
