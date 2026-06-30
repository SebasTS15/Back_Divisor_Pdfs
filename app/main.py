from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.app_metadata import OPENAPI_CONFIG
from app.core.middlewere import loggin_middlewere
from .core.logging import setup_logging, logger
from .router import router_pdf_service

setup_logging()

@asynccontextmanager
async def life_span(app:FastAPI):
    logger.info('Iniciando aplicación...')
    yield
    logger.info('Cerrando aplicación...')



app = FastAPI(
    **OPENAPI_CONFIG,
    lifespan=life_span
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(loggin_middlewere)

app.include_router(router_pdf_service, prefix="/api")

