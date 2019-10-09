import pytest

from inode import Inode
from ._utils import filesystem, gen_stream


CONTENT = b'hello world'
MIME = 'text/plain'


@pytest.mark.asyncio
async def test_inode(filesystem):
    stream = gen_stream(CONTENT)
    inode = await Inode.create(stream, MIME)
    assert inode.mime == MIME
    assert inode.ref_count == 1

    chunks = []
    async for chunk in inode.stream:
        chunks.append(chunk)
    assert CONTENT == b''.join(chunks)

    stream = gen_stream(CONTENT)
    inode = await Inode.create(stream, 'asdf')
    assert inode.mime == MIME
    assert inode.ref_count == 2

    inode.ref()
    assert inode.ref_count == 3

    inode.unref()
    assert inode.ref_count == 2

    inode.unref()
    assert inode.ref_count == 1

    inode.unref()
    assert not inode
