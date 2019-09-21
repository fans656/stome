import os
import shutil
import importlib

import conf


def test_default_root_dir():
    shutil.rmtree(conf.ROOT_DIR)
    importlib.reload(conf)
    for path in (
            conf.ROOT_DIR,
            conf.META_DIR,
            conf.INODE_DATA_DIR,
            conf.INODE_META_DIR,
            conf.TEMP_DIR,
    ):
        assert os.path.exists(path)
