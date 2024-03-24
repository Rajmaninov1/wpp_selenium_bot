from os import getcwd
from pathlib import Path

from fastapi import APIRouter, status as fapi_status, UploadFile, File
from fastapi.responses import ORJSONResponse
from pydantic_extra_types.phone_numbers import PhoneNumber

from config.constants import IMGS_LOCATION, VIDEOS_LOCATION, FILES_LOCATION
from services.wpp_web_bot.wrapper import wpp_wrapper

router = APIRouter()


@router.get(
    '/send_text_message/{phone}/{message}',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK,
)
async def post_send_text_message(phone: PhoneNumber, message: str):
    if not wpp_wrapper.login():
        try:
            if not wpp_wrapper.find_user(phone):
                return {'error': 'user not found'}
            else:
                wpp_wrapper.send_message(message)
        except Exception as e:
            return {'error': str(e)}
        return {'success': 'message sent', 'error': None}
    return {'error': 'First login in your whatsapp account'}


@router.post(
    '/send_img_message/{phone}/{message}',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK,
)
async def post_send_img_message(
        phone: PhoneNumber,
        message: str, img:
        UploadFile = File(..., description='Only image files')
):
    if not img.content_type.startswith('image'):
        return {'error': 'Incorrect file type'}
    img_path = IMGS_LOCATION + img.filename
    with open(img_path, "wb+") as file_object:
        file_object.write(img.file.read())
    if not wpp_wrapper.login():
        try:
            if not wpp_wrapper.find_user(phone):
                return {'error': 'user not found'}
            else:
                wpp_wrapper.send_picture(picture=Path(f'{getcwd()}/{img_path}'), message=message)
        except Exception as e:
            return {'error': str(e)}
        return {'success': 'message sent', 'error': None}
    return {'error': 'First login in your whatsapp account'}


@router.post(
    '/send_video_message/{phone}/{message}',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK,
)
async def post_send_video_message(
        phone: PhoneNumber,
        message: str,
        video: UploadFile = File(..., description='Only video .mp4, .3gpp and .quicktime')
):
    if video.content_type not in ['video/mp4', 'video/3gpp', 'video/quicktime']:
        return {'error': 'Incorrect file type'}
    video_path = VIDEOS_LOCATION + video.filename
    with open(video_path, "wb+") as file_object:
        file_object.write(video.file.read())
    if not wpp_wrapper.login():
        try:
            if not wpp_wrapper.find_user(phone):
                return {'error': 'user not found'}
            else:
                wpp_wrapper.send_video(video=Path(f'{getcwd()}/{video_path}'), message=message)
        except Exception as e:
            return {'error': str(e)}
        return {'success': 'message sent', 'error': None}
    return {'error': 'First login in your whatsapp account'}


@router.post(
    '/send_file_message/{phone}/{message}',
    response_class=ORJSONResponse,
    status_code=fapi_status.HTTP_200_OK,
)
async def post_send_file_message(phone: PhoneNumber, message: str, file: UploadFile = File(...)):
    file_path = FILES_LOCATION + file.filename
    with open(file_path, "wb+") as file_object:
        file_object.write(file.file.read())
    if not wpp_wrapper.login():
        try:
            if not wpp_wrapper.find_user(phone):
                return {'error': 'user not found'}
            else:
                wpp_wrapper.send_file(filename=Path(f'{getcwd()}/{file_path}'), message=message)
        except Exception as e:
            return {'error': str(e)}
        return {'success': 'message sent', 'error': None}
    return {'error': 'First login in your whatsapp account'}
