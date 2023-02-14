from fastapi import Depends, FastAPI, Request

import app.logger
from app.internal import admin
from app.routers import manifest
from app.dependencies import get_db
from app.seed_db import seed_api_keys
from app.models import Base
from app.database import engine

logger = app.logger.logger(__name__)

Base.metadata.create_all(bind=engine)

seed_api_keys()

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(admin.router)
app.include_router(manifest.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"start request path={request.url.path}")
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "file upload service"}