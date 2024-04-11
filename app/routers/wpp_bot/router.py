from fastapi import FastAPI, APIRouter

from .browser_session import router as wpp_browser_session_include_router
from .login import router as wpp_login_include_router
from .send_messages import router as wpp_send_include_router
from .get_messages import router as wpp_get_messages_router


def include_router(app: FastAPI):
    api_router = APIRouter()
    api_router.include_router(wpp_login_include_router, prefix='/login', tags=['Whatsapp Web'])
    api_router.include_router(wpp_send_include_router, prefix='/send', tags=['Whatsapp Web'])
    api_router.include_router(wpp_get_messages_router, prefix='/get', tags=['Whatsapp Web'])
    api_router.include_router(wpp_browser_session_include_router, prefix='/session', tags=['Whatsapp Web'])
    app.include_router(api_router, prefix='/wpp_bot')
