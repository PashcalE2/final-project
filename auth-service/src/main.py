from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.endpoints import router
from src.exception import AppException


app = FastAPI(
    title="Auth service",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


app.include_router(router=router)


def handle_default_error(
    exc: Exception,
    status_code: int,
    headers: dict | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"detail": str(exc)}, headers=headers
    )


@app.exception_handler(AppException)
async def app_exception_handler(req: Request, exc: AppException) -> JSONResponse:
    return handle_default_error(exc, status_code=exc.status_code)
