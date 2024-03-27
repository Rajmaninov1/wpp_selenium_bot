from fastapi import FastAPI, APIRouter

from .read import router as send_messages_router


def include_router(app: FastAPI):
    api_router = APIRouter()
    api_router.include_router(send_messages_router, prefix="/read", tags=['Google Sheets'])
    app.include_router(api_router, prefix='/google_sheets')
