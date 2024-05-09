from fastapi import APIRouter, status as fapi_status
from fastapi.responses import ORJSONResponse
from pydantic_extra_types.phone_numbers import PhoneNumber

from services.wpp_web_bot.wrapper import wpp_wrapper

router = APIRouter()

@router.get(
    '/get_text_messages/',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK,
)
async def get_get_text_messages(phone: PhoneNumber):
    if not wpp_wrapper.login():
        try:
            if not wpp_wrapper.find_user(phone):
                return {'error': 'user not found'}
            else:
                return wpp_wrapper.get_messages()
        except Exception as e:
            return {'error': str(e)}
    return {'error': 'First login in your whatsapp account'}
