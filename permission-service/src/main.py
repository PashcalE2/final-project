from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.endpoints import router
from src.api.rabbitmq import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with broker:
        yield


app = FastAPI(
    title="Permission service",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)


app.include_router(router=router)
