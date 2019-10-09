import imp
import shutil

import pytest

import conf


@pytest.fixture
def filesystem():
    imp.reload(conf)
    yield
    shutil.rmtree(conf.ROOT_DIR)


async def gen_stream(content: bytes):
    i = 0
    while i < len(content):
        yield content[i:i+conf.CHUNK_SIZE]
        i += conf.CHUNK_SIZE
