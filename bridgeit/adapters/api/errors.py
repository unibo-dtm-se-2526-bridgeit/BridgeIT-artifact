"""Shared error format for the API.

All endpoints should raise ApiError instead of FastAPI's plain
HTTPException, so every error response follows the same shape:

    {"error": {"code": "...", "message": "..."}}

`code` is a stable, machine-readable identifier (not meant to be shown
directly to end users); `message` is a human-readable description.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """Raised by route handlers to produce a structured error response."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


def register_error_handlers(app: FastAPI) -> None:
    """Register the ApiError -> JSON response mapping on the given app."""

    @app.exception_handler(ApiError)
    async def handle_api_error(_: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )
