from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from node import Node, File, Dir
from utils import get_user


app = FastAPI(
    title='stome',
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)


@app.get('/api/file/{path:path}')
async def download_file(path):
    f = File(path)
    ensure_existed(f)
    ensure_is_file(f)
    inode = f.inode
    return StreamingResponse(inode.stream, media_type=inode.mime)


@app.post('/api/file/{path:path}')
async def upload_file(path, request: Request):
    ensure_me(request)
    f = File(path)
    if f:
        ensure_is_file(f)
        f.delete()
    await f.create(request.stream())


def ensure_existed(node):
    if not node:
        raise HTTPException(404, 'Not found')


def ensure_type(node, type):
    if node.type != type:
        raise HTTPException(400, f'Node is {node.type} instead of {type}')


def ensure_is_file(node):
    ensure_type(node, 'file')


def ensure_is_dir(node):
    ensure_type(node, 'dir')


def ensure_me(request):
    user = get_user(request)
    if user['username'] != 'fans656':
        raise HTTPException(401, 'require fans656 login')


app.mount('/', StaticFiles(directory='../frontend/out/', html=True))
