from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.base import BaseAppException
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(BaseAppException)
    async def base_exception_handler(
        request: Request,
        exc: BaseAppException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": request.url.path,
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:

        if exc.status_code == HTTPStatus.NOT_FOUND:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={
                    "error": {
                        "code": "ROUTE_NOT_FOUND",
                        "message": "The requested endpoint does not exist",
                        "path": request.url.path,
                    }
                },
            )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "path": request.url.path,
                }
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        logger.exception(
            "Unhandled exception while processing %s %s",
            request.method,
            request.url,
        )

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Something went wrong",
                    "path": request.url.path,
                }
            },
        )
