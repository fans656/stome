import os


CHUNK_SIZE = 4096
PUBKEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDP6Sm7IYP9/1SwvgAnIK8+omG5WeK4ZmEeSrAbjtPsqw8JtfbXAI8/IlaOv9EK+jjZ6A0KOH3LvnmpbAZVgK0PaDbNXiNE6ZXs5Z26Yt9peTWD4tKEZoBNc0M0TvLv5RK2MQCYOEHrdJODGh4MLqhC58QT3SbL3TE0jCgo7rqf2aQkrX+gwDynnjBkzh8/GUmWT6XK2SYn/d4bWJ7Xrf37Rj+hIEvnO1NEETlrIljGg0XuFjLXLxdXoKv69XZ0G0avypcq+6BYzgy9bghySviwwGCA2k9eaOSt2iKf6J8H4laSyR2SC7AJMfe3zNeNTlwTrp4frkRr6Mzc2+zI0erP'


ROOT_DIR = None
META_DIR = None
TEMP_DIR = None
INODE_DATA_DIR = None
INODE_META_DIR = None
META_DIR_PREFIX_LENGTH = None


def setup_root_dir(path=None):
    global ROOT_DIR, META_DIR, TEMP_DIR, INODE_DATA_DIR, INODE_META_DIR, META_DIR_PREFIX_LENGTH

    ROOT_DIR = os.path.abspath(path)
    META_DIR = os.path.join(ROOT_DIR, 'meta')
    TEMP_DIR = os.path.join(ROOT_DIR, 'temp')
    INODE_DATA_DIR = os.path.join(ROOT_DIR, 'inode-data')
    INODE_META_DIR = os.path.join(ROOT_DIR, 'inode-meta')
    META_DIR_PREFIX_LENGTH = len(META_DIR)

    for path in (META_DIR, TEMP_DIR, INODE_DATA_DIR, INODE_META_DIR):
        if not os.path.exists(path):
            os.makedirs(path)


setup_root_dir(os.environ.get('ROOT', '/data/stome-root'))
