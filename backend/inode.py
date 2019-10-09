"""
An `Inode` is represented by 2 files:
    1. Data file has the actual content,
       e.g. /stome/inode-data/d41d8cd98f00b204e9800998ecf8427e
    2. Meta file has the meta info, like `ref_count`, `mime` type, etc...
       e.g. /stome/inode-meta/d41d8cd98f00b204e9800998ecf8427e
The file name is MD5 hash of the actual content.
"""
import os
import typing

import conf
from utils import save_json, load_json, save_stream, load_stream


class Inode:

    @staticmethod
    async def create(
        stream: typing.AsyncGenerator[bytes, None],
        mime: str,
    ) -> 'Inode':
        """
        Given a stream and MIME type, save the content into a file and create an Inode.
        """
        fpath, md5 = await save_stream(stream)
        inode = Inode(md5)
        try:
            if not inode:
                os.rename(fpath, inode.data_path)
                inode.meta = {
                    'ref_count': 1,
                    'mime': mime,
                }
                inode._save_meta()
            else:
                inode.ref()
        finally:
            if os.path.exists(fpath):
                os.remove(fpath)
        return inode

    def __init__(self, md5: str):
        self.md5 = md5
        self.data_path = os.path.join(conf.INODE_DATA_DIR, md5)
        self.meta_path = os.path.join(conf.INODE_META_DIR, md5)
        self.meta = load_json(self.meta_path, {})

    def __bool__(self):
        return os.path.isfile(self.data_path)

    @property
    def mime(self) -> str:
        return self.meta['mime']

    @property
    def ref_count(self) -> int:
        return self.meta['ref_count']

    @property
    def stream(self) -> typing.AsyncGenerator[bytes, None]:
        return load_stream(self.data_path)

    def ref(self):
        self.meta['ref_count'] += 1
        self._save_meta()

    def unref(self):
        self.meta['ref_count'] -= 1
        if self.meta['ref_count'] > 0:
            self._save_meta()
        else:
            self._remove()

    def _save_meta(self):
        save_json(self.meta, self.meta_path)

    def _remove(self):
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        if os.path.exists(self.meta_path):
            os.remove(self.meta_path)
