from fastapi import APIRouter, status as fapi_status
from fastapi.responses import Response

from services.wpp_web_bot.wrapper import wpp_wrapper

router = APIRouter()


@router.get(
    '/get_qr',
    response_class=Response,
    status_code=fapi_status.HTTP_200_OK,
)
async def get_qr_wpp():
    qr = wpp_wrapper.login()
    return Response(content=qr, media_type="image/png") if qr else ''
