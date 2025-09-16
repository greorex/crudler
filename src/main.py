import os
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlmodel import SQLModel
from dotenv import load_dotenv

logger = logging.getLogger("uvicorn.error")

load_dotenv(
    os.environ.get("ENV_FILE", ".test.env"),
    override=True,
)

from .db import create_db_and_tables
from .routers.crudl import CRUDLRouter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up...")
    await create_db_and_tables()
    yield
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)


def import_class(name: str, _from: str = None):
    p = list(map(lambda x: x.replace("/", "."), name.split(".")))
    if len(p) < 2:
        p.append(p[0])
    if len(p) < 3:
        p.insert(0, _from)
    return getattr(__import__(".".join(p[:2]), fromlist=p[1:2]), p[2])


logger.info("Models:")
models = list(filter(lambda x: x, os.environ.get("MODELS", "").split()))
for model in models:
    Model = import_class(model, os.environ.get("MODELS_PATH", "models"))
    if issubclass(Model, SQLModel):
        logger.info(f"- {model}")
        app.include_router(CRUDLRouter(Model))


@app.get("/")
def read_root():
    """
    A simple CRUDL endpoint.
    """
    return {
        "message": "CRUDL endpoint",
    }
