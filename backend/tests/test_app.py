import os
import shutil

import pytest
from starlette.testclient import TestClient

import app
import conf


NON_EXISTED_DIR = '/NON_EXISTED_DIR'
NON_EXISTED_FILE = '/NON_EXISTED_FILE'
EXISTED_DIR = '/'
EXISTED_FILE = '/EXISTED_FILE'
TEXT_CONTENT = b'TEXT_CONTENT'
BINARY_CONTENT = b'\01\02\03'

JPG_FILE = '/JPG_FILE.jpg'
JPG_CONTENT = 'JPG_CONTENT'

MP3_FILE = '/MP3_FILE.mp3'
MP3_CONTENT = 'MP3_CONTENT'

MP4_FILE = '/MP4_FILE.mp4'
MP4_CONTENT = 'MP4_CONTENT'


@pytest.fixture
def client():
    return TestClient(app.app)


@pytest.fixture
def authed():
    _get_user = app.get_user
    app.get_user = lambda *args, **kwargs: {'username': 'fans656'}
    yield
    app.get_user = _get_user


@pytest.fixture
def filesystem():
    conf.ROOT_DIR = '/tmp/stome-root'
    if os.path.exists(conf.ROOT_DIR):
        shutil.rmtree(conf.ROOT_DIR)
    conf.setup_root_dir(conf.ROOT_DIR)
    yield
    shutil.rmtree(conf.ROOT_DIR)


def test_index_should_return_html(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.headers['content-type'].startswith('text/html')


def test_invalid_download(client, filesystem):
    assert client.get('/api/file' + NON_EXISTED_DIR).status_code == 404
    assert client.get('/api/file' + NON_EXISTED_FILE).status_code == 404
    assert client.get('/api/file' + EXISTED_DIR).status_code == 400


def test_upload_and_download(client, filesystem, authed):
    # text content
    assert client.post('/api/file' + EXISTED_FILE, data=TEXT_CONTENT).status_code == 200
    assert client.get('/api/file' + EXISTED_FILE).content == TEXT_CONTENT
    # binary content
    assert client.post('/api/file' + EXISTED_FILE, data=BINARY_CONTENT).status_code == 200
    assert client.get('/api/file' + EXISTED_FILE).content == BINARY_CONTENT


def test_mime_type(client, filesystem, authed):
    assert client.post('/api/file' + JPG_FILE, data=JPG_CONTENT).status_code == 200
    assert client.get('/api/file' + JPG_FILE).headers['content-type'] == 'image/jpeg'

    assert client.post('/api/file' + MP3_FILE, data=MP3_CONTENT).status_code == 200
    assert client.get('/api/file' + MP3_FILE).headers['content-type'] == 'audio/mpeg'

    assert client.post('/api/file' + MP4_FILE, data=MP4_CONTENT).status_code == 200
    assert client.get('/api/file' + MP4_FILE).headers['content-type'] == 'video/mp4'


def test_auth(client):
    # upload requires auth
    assert client.post('/api/file').status_code == 405
    assert client.post('/api/file' + NON_EXISTED_DIR).status_code == 401
    assert client.post('/api/file' + NON_EXISTED_FILE).status_code == 401
    assert client.post('/api/file' + EXISTED_DIR).status_code == 401
    assert client.post('/api/file' + EXISTED_FILE).status_code == 401
