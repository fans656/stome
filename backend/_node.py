import os
import json
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

    def move(self, dst: 'Node'):
        dir_path = os.path.dirname(dst.path)
        dst_dir = Dir(dir_path)
        if not dst_dir:
            dst_dir.create()
        os.replace(self.abspath, dst.abspath)

    def delete(self):
        if self.type == NodeType.Dir:
            Dir(self.path).delete()
        else:
            File(self.path).delete()

    def __bool__(self):
        return os.path.exists(self.abspath)

    def __lt__(self, o):
        return self.name < o.name

    def __iter__(self):
        return iter([
            ('type', self.type),
            ('path', self.path),
            ('name', self.name),
        ])


class Dir(Node):

    def create(self):
        os.makedirs(self.abspath)

    def delete(self):
        for node in self.children:
            node.delete()
        os.rmdir(self.abspath)

    def list(self):
        return sorted(self.dirs), sorted(self.files)

    @property
    def dirs(self):
        return [Dir(node.path) for node in self.children if node.type == 'dir']

    @property
    def files(self):
        return [File(node.path) for node in self.children if node.type == 'file']

    @property
    def children(self):
        return [Node(os.path.join(self.path, fname)) for fname in os.listdir(self.abspath)]



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
        inode = await Inode.create(stream, _get_mime(self.name))
        # init meta
        self.save_meta({
            'inode': inode.md5,
        })

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


def _get_mime(fname):
    mime, encoding = mimetypes.guess_type(fname)
    return mime or 'application/octet-stream'


if __name__ == '__main__':
    print(_absolute_path('/'))
    print(_absolute_path(''))
