import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.base import BaseAppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(BaseAppException)
    async def base_exception_handler(
        request: Request,
        exc: BaseAppException,
    ) -> JSONResponse:

        # Log handled application exceptions.
        logger.error(
            "Application exception | " "Code: %s | Message: %s | Method: %s | Path: %s",
            exc.error_code,
            exc.message,
            request.method,
            request.url.path,
        )

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

            # Log requests to non-existent routes.
            logger.warning(
                "Route not found | Method: %s | Path: %s",
                request.method,
                request.url.path,
            )

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

        # Log handled HTTP exceptions.
        logger.warning(
            "HTTP exception | " "Status: %s | Method: %s | Path: %s | Message: %s",
            exc.status_code,
            request.method,
            request.url.path,
            exc.detail,
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

        # Log unexpected exceptions with the full traceback.
        logger.exception(
            "Unhandled exception | Method: %s | Path: %s",
            request.method,
            request.url.path,
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
