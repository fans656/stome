from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


app = FastAPI(
    title='stome',
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)


app.mount('/', StaticFiles(directory='../frontend/out/', html=True))
