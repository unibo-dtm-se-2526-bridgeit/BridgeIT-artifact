"""Shared error format for the API.

All endpoints should raise ApiError instead of FastAPI's plain
HTTPException, so every error response follows the same shape:

    {"error": {"code": "...", "message": "..."}}

`code` is a stable, machine-readable identifier (not meant to be shown
directly to end users); `message` is a human-readable description.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """Raised by route handlers to produce a structured error response."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


def register_error_handlers(app: FastAPI) -> None:
    """Register error handlers so every error response follows the shared shape."""

    @app.exception_handler(ApiError)
    async def handle_api_error(_: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Pydantic/FastAPI's default validation error format is a list of
        # per-field issues. We summarize it into a single, structured
        # message consistent with ApiError, instead of exposing FastAPI's
        # raw shape to API clients.
        first_error = exc.errors()[0]
        field = ".".join(str(part) for part in first_error["loc"] if part != "body")
        message = f"Invalid value for '{field}': {first_error['msg']}"
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "missing_field", "message": message}},
        )
