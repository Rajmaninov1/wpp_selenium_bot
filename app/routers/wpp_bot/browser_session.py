from fastapi import APIRouter, status as fapi_status
from fastapi.responses import ORJSONResponse

from services.wpp_web_bot.wrapper import wpp_wrapper

router = APIRouter()


@router.get(
    '/close_session',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK
)
async def get_close_session():
    try:
        wpp_wrapper.browser.quit()
        wpp_wrapper.browser_open = False
        return {'response': 'session successfully closed'}
    except Exception as e:
        return {'errors': f'Can\'t close the session: {str(e)}'}


@router.get(
    '/start_session',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK
)
async def get_start_session():
    try:
        if not wpp_wrapper.browser_open:
            wpp_wrapper.__init__()
        return {'response': 'session successfully started'}
    except Exception as e:
        return {'errors': f'Can\'t start the session: {str(e)}'}