from fastapi import FastAPI

from .google_sheets.router import include_router as google_sheets_include_router
from .wpp_bot.router import include_router as wpp_bot_include_router


def add_routers(app: FastAPI) -> None:
    google_sheets_include_router(app)
    wpp_bot_include_router(app)
