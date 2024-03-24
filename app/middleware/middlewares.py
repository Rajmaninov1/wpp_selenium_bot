from fastapi import FastAPI

from .error_handlers.api import add_handler as api_add_handler
from .error_handlers.pydantic_error import pydantic_add_handler


def add_error_handlers(app: FastAPI) -> None:
    api_add_handler(app)
    pydantic_add_handler(app)
