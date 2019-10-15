"""
Node is a filesystem entity, either directory or file.
Node can be:
    - Created
    - Moved
    - Deleted
File can:
    - Retrieve Inode
File meta has:
    - inode_md5: MD5 hash of its Inode content
Dir can be:
    - Listed
Dir meta is not supported yet.
"""
import os
import json
import typing
import mimetypes

import conf
from inode import Inode
from utils import load_json, save_json


class Node:

    def __init__(self, path: str):
        self._set_path(path)

    @property
    def meta(self) -> dict:
        return load_json(self.abspath, {})

    def save_meta(self, meta: dict = None):
        save_json(meta or self.meta, self.abspath)

    @property
    def type(self) -> str:
        return 'dir' if os.path.isdir(self.abspath) else 'file'

    def move(self, dst: 'Node'):
        if self.path == '/':
            raise RuntimeError('root dir can not be moved')
        dst_dir = Dir(os.path.dirname(dst.path))
        if not dst_dir:
            dst_dir.create()
        os.replace(self.abspath, dst.abspath)
        self._set_path(dst.path)

    def delete(self):
        if self.path == '/':
            raise RuntimeError('root dir can not be deleted')
        if self.type == 'dir':
            Dir(self.path).delete()
        else:
            File(self.path).delete()

    def __bool__(self):
        return os.path.exists(self.abspath)

    def __lt__(self, o):
        return self.path < o.path

    def __iter__(self):
        return iter([
            ('type', self.type),
            ('path', self.path),
            ('name', self.name),
        ])

    def _set_path(self, path):
        self.abspath = _absolute_path(path)
        self.path = _external_path(self.abspath)
        self.name = os.path.basename(self.path)


class Dir(Node):

    def create(self):
        os.makedirs(self.abspath)

    def delete(self):
        for node in self.children:
            node.delete()
        os.rmdir(self.abspath)

    def list(self):
        return self.dirs, self.files

    @property
    def dirs(self):
        return sorted([Dir(node.path) for node in self.children if node.type == 'dir'])

    @property
    def files(self):
        return sorted([File(node.path) for node in self.children if node.type == 'file'])

    @property
    def children(self):
        return [Node(os.path.join(self.path, fname)) for fname in os.listdir(self.abspath)]



class File(Node):

    @property
    def inode(self) -> typing.Optional[Inode]:
        inode_id = self.meta.get('inode_md5')
        return Inode(inode_id) if inode_id else None

    async def create(self, stream: typing.AsyncGenerator[bytes, None]):
        # ensure parent directory exists
        d = Dir(os.path.dirname(self.path))
        if not d:
            d.create()
        # ensure old inode removed
        inode = self.inode
        if inode:
            inode.unref()
        # create new inode
        inode = await Inode.create(stream, _guess_mime(self.name))
        # init meta
        self.save_meta({
            'inode_md5': inode.md5,
        })
        return self

    def delete(self):
        self.inode.unref()
        if os.path.exists(self.abspath):
            os.remove(self.abspath)


def _absolute_path(path):
    """
    Convert external path to local filesystem path.
    Raise `RuntimeError` if the resulting path is out of root directory.
    >>> _absolute_path('/foo/bar') === '/data/stome-root/foo/bar'
    >>> _absolute_path('foo/bar') === '/data/stome-root/foo/bar'
    """
    if path.startswith('/'):
        path = path[1:]
    path = os.path.join(conf.META_DIR, path)
    path = os.path.abspath(path)
    if not path.startswith(conf.META_DIR):
        raise RuntimeError(f'invalid path {path}')
    return path


def _external_path(abspath):
    return abspath[conf.META_DIR_PREFIX_LENGTH:] or '/'


def _guess_mime(fname):
    mime, encoding = mimetypes.guess_type(fname)
    return mime or 'application/octet-stream'
