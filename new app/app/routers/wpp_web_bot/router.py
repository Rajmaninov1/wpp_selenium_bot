from fastapi import FastAPI, APIRouter

from .send_messages import router as send_messages_router


def include_router(app: FastAPI):
    api_router = APIRouter()
    api_router.include_router(send_messages_router, prefix="/send_messages", tags=['Send Messages'])
    app.include_router(api_router, prefix='/wpp_bot')
