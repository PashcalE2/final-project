from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.endpoints import router
from src.api.rabbitmq import broker, request_queue, response_queue


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with broker:
        await broker.declare_queue(request_queue)
        await broker.declare_queue(response_queue)
        await broker.start()
        yield
        await broker.stop()


app = FastAPI(
    title="Request service",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)


app.include_router(router=router)
