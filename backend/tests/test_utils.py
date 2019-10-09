import os
import hashlib

import pytest

from utils import save_json, load_json, save_stream, load_stream
from ._utils import filesystem, gen_stream


PATH = '/tmp/t.json'
INVALID_PATH = '/tmp/not-existed.json'
DATA = {'a': 3, 'b': 5}
CONTENT = """\
{
  "a": 3,
  "b": 5
}"""


def test_save_json():
    save_json(DATA, PATH)
    with open(PATH) as f:
        assert f.read() == CONTENT
    os.remove(PATH)


def test_load_json():
    with open(PATH, 'w') as f:
        f.write(CONTENT)
    assert load_json(PATH) == DATA
    os.remove(PATH)


def test_load_json_with_default():
    assert load_json(INVALID_PATH) == {}
    assert load_json(INVALID_PATH, {'foo': 'bar'}) == {'foo': 'bar'}


@pytest.mark.asyncio
async def test_stream(filesystem):
    await assert_stream(b'hello world')
    await assert_stream(b'\0\1\2')
    await assert_stream(b'\0\1' * 1024 * 1024)


async def assert_stream(content):
    stream = gen_stream(content)
    fpath, md5 = await save_stream(stream)
    with open(fpath, 'rb') as f:
        actual_content = f.read()

    assert actual_content == content

    h = hashlib.md5()
    h.update(actual_content)
    assert h.hexdigest() == md5

    chunks = []
    async for chunk in load_stream(fpath):
        chunks.append(chunk)
    assert content == b''.join(chunks)
