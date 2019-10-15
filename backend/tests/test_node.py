import pytest

from node import Node, File, Dir
from ._utils import filesystem, gen_stream


CONTENT = b'hello world'


def test_root_dir():
    root = Node('/')
    assert root
    assert root.type == 'dir'
    with pytest.raises(RuntimeError):
        assert root.move(None)
    with pytest.raises(RuntimeError):
        assert root.delete()


def test_dict():
    node = Node('/')
    info = dict(node)
    assert 'type' in info
    assert 'path' in info
    assert 'name' in info


@pytest.mark.asyncio
async def test_file(filesystem):
    # create
    node = await File('/test.txt').create(gen_stream(CONTENT))
    assert node
    inode = node.inode
    assert inode
    # rename
    node.move(Node('/foo.txt'))
    assert Node('/foo.txt')
    assert not Node('/test.txt')
    # move
    node.move(Node('/temp/test.txt'))
    assert Node('/temp/test.txt')
    assert not Node('/foo.txt')
    # delete
    node.delete()
    assert not node
    assert not inode


@pytest.mark.asyncio
async def test_dir(filesystem):
    # create
    node = Dir('/foo')
    node.create()
    assert node
    # rename
    node.move(Node('/bar'))
    assert Node('/bar')
    assert not Node('/foo')
    # move
    node.move(Node('/temp/foo'))
    assert Node('/temp/foo')
    assert not Node('/bar')
    node.move(Node('/foo'))
    # list
    Dir('/foo/bar/baz').create()
    await File('/foo/test.txt').create(gen_stream(CONTENT))
    dirs, files = node.list()
    assert len(dirs) == 1
    assert dirs[0].path == '/foo/bar'
    assert len(files) == 1
    assert files[0].path == '/foo/test.txt'
    # delete
    node.delete()
    assert not node
    assert not Node('/foo/bar/baz')
    assert not Node('/foo/bar')
    assert not Node('/foo/test.txt')
