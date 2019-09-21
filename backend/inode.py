import os
import typing

import conf
from utils import save_json, load_json, save_stream, load_stream


class Inode:

    @staticmethod
    async def create(stream, mime):
        return await create_inode(stream, mime)

    def __init__(self, md5: str):
        self.md5 = md5
        self.data_path = os.path.join(conf.INODE_DATA_DIR, md5)
        self.meta_path = os.path.join(conf.INODE_META_DIR, md5)
        self.meta = load_json(self.meta_path, {})

    def __bool__(self):
        return os.path.isfile(self.meta_path)

    @property
    def mime(self) -> str:
        return self.meta['mime']

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


async def create_inode(
    stream: typing.AsyncGenerator[bytes, None],
    mime: str,
) -> Inode:
    fpath, md5 = await save_stream(stream)
    try:
        inode = Inode(md5)
        if inode:
            inode.ref()
        else:
            os.rename(fpath, inode.data_path)
            inode.meta = {
                'ref_count': 1,
                'mime': mime,
            }
            inode._save_meta()
        return inode
    finally:
        if os.path.exists(fpath):
            os.remove(fpath)
