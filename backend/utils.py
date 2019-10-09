import os
import json
import uuid
import typing
import hashlib

import aiofiles

import conf


def save_json(data: dict, path: str):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def load_json(path: str, default_data: dict = None):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default_data or {}


async def load_stream(path: str) -> typing.AsyncGenerator[bytes, None]:
    """
    Given a file path, load the content as an async stream.
    """
    async with aiofiles.open(path, 'rb') as f:
        while True:
            chunk = await f.read(conf.CHUNK_SIZE)
            if not chunk:
                break
            yield chunk


async def save_stream(stream: typing.AsyncGenerator[bytes, None]) -> typing.Tuple[str, str]:
    """
    Given a stream, save into a temporary file
    (e.g. /data/stome-root/temp/973faa14-e835-473a-9a8f-8a70ef166f9c).
    Return the file path and MD5 hash.
    """
    fpath = os.path.join(conf.TEMP_DIR, str(uuid.uuid4()))
    hasher = hashlib.md5()
    async with aiofiles.open(fpath, 'wb') as f:
        async for chunk in stream:
            await f.write(chunk)
            hasher.update(chunk)
    return fpath, hasher.hexdigest()
