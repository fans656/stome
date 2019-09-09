import pytest
from starlette.testclient import TestClient

import app


@pytest.fixture
def client():
    return TestClient(app.app)


def test_index_should_return_html(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.headers['content-type'].startswith('text/html')
