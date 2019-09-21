from fastapi import FastAPI, HTTPException
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import StreamingResponse

from node import Node, File
from utils import get_user


app = FastAPI(
    title='stome',
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)


@app.get('/api/file/{path:path}')
async def download_file(path, request: Request):
    f = File(path)
    ensure_existed(f)
    ensure_file(f)
    inode = f.inode
    return StreamingResponse(inode.stream, media_type=inode.mime)


@app.post('/api/file/{path:path}')
async def upload_file(path, request: Request):
    ensure_me(request)
    f = File(path)
    ensure_file(f)
    await f.create(request.stream())


app.mount('/', StaticFiles(directory='../frontend/out/', html=True))


def ensure_me(request):
    user = get_user(request)
    if user['username'] != 'fans656':
        raise HTTPException(401, 'Require fans656 login')


def ensure_existed(node):
    if not node:
        raise HTTPException(404, 'Not found')


def ensure_file(node):
    if node.type != 'file':
        raise HTTPException(400, f'"{node.path}" is not file')
