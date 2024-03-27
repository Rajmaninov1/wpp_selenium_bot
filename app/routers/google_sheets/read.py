from fastapi import APIRouter, status as fapi_status
from fastapi.responses import ORJSONResponse

from schemas.google_sheets.columns import WorkSheetColumnNameEnum, WorkSheetColumnEnum
from services.google_sheets.spreadsheets import SpreadSheet

router = APIRouter()


@router.get(
    '/gsheets/document/{document_name}/sheet/{sheet_name}/column/{column}',
    response_class=ORJSONResponse,
    response_model=dict,
    status_code=fapi_status.HTTP_200_OK,
)
async def get_read_document_sheet(document_name: str, sheet_name: str, column: WorkSheetColumnNameEnum):
    return SpreadSheet(
        document_name=document_name, sheet_name=sheet_name
    ).get_column(column=WorkSheetColumnEnum(column))
