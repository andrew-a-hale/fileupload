import logging
from fastapi import Depends, FastAPI, Request

from app.logger import setup_logger
from app.internal import admin
from app.routers import manifest, bucket, payload
from app.dependencies import get_db, check_api_key
from app.seed_db import setup_db

setup_logger(logging.DEBUG)
setup_db()

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(admin.router, dependencies=[Depends(check_api_key)])
app.include_router(manifest.router)
app.include_router(bucket.router)
app.include_router(payload.router)


@app.middleware('http')
async def log_requests(request: Request, call_next):
    logging.info(f'{request.method} {request.url.path}')
    response = await call_next(request)
    return response


@app.get('/')
async def root():
    return {'message': 'file upload service'}