from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.exceptions.base import BaseAppException


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
                }
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Something went wrong",
                }
            },
        )
