import os
import mimetypes

import conf
from inode import Inode
from utils import load_json, save_json


class Node:

    def __init__(self, path):
        self.abspath = _absolute_path(path)
        self.path = _external_path(self.abspath)
        self.name = os.path.basename(self.path)

    @property
    def meta(self):
        return load_json(self.abspath, {})

    def save_meta(self, meta=None):
        save_json(meta or self.meta, self.abspath)

    @property
    def type(self):
        return 'dir' if os.path.isdir(self.abspath) else 'file'

    def __bool__(self):
        return os.path.exists(self.abspath)

    def __lt__(self, o):
        return self.name < o.name


class Dir(Node):

    def create(self):
        os.makedirs(self.abspath)


class File(Node):

    @property
    def inode(self):
        inode_id = self.meta.get('inode')
        return Inode(inode_id) if inode_id else None

    async def create(self, stream):
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
        self.save_meta({'inode': inode.md5})


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
