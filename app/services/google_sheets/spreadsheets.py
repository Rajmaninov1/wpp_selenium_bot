from datetime import datetime
from typing import Any

import gspread
from google.oauth2.service_account import Credentials
from gspread import Spreadsheet, WorksheetNotFound
from pydantic import ValidationError

from config.exceptions import ColumnNotFoundException, IncorrectTypeException
from schemas.google_sheets.columns import WorkSheetColumnEnum


def open_document(document_name: str) -> Spreadsheet:
    """ """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        "private_files/keys/Keys.json", scopes=scopes
    )

    return gspread.authorize(credentials).open(document_name)


class SpreadSheet:
    """ """

    def __init__(
            self,
            *,
            document_name: str,
            sheet_name: str
    ):
        self.document_name: str = document_name
        self.sheet_name: str = sheet_name
        self.document: Spreadsheet = open_document(self.document_name)
        self.sheet_number: int = self._get_sheets_names().index(sheet_name)

    def sheet_verification(
            self,
            *,
            sheet_name: str
    ):
        """ """
        if sheet_name is not None:
            sheets_names = self._get_sheets_names()
            if sheet_name in sheets_names:
                self.sheet_name = sheet_name
                self.sheet_number = sheets_names.index(sheet_name)
            else:
                raise WorksheetNotFound
        else:
            raise WorksheetNotFound

    def get_column(
            self,
            *,
            column: WorkSheetColumnEnum,
            sheet_name: str = None
    ) -> list[str | int | float]:
        """ """
        try:
            self.sheet_verification(sheet_name=sheet_name if sheet_name else self.sheet_name)
            if column == WorkSheetColumnEnum.PHONES:
                return self.document.get_worksheet(self.sheet_number).col_values(3)[1:]
            elif column == WorkSheetColumnEnum.APPROVALS:
                return self.document.get_worksheet(self.sheet_number).col_values(4)[1:]
            elif column == WorkSheetColumnEnum.SEND_VERIFICATIONS:
                return self.document.get_worksheet(self.sheet_number).col_values(5)[1:]
            elif column == WorkSheetColumnEnum.DATE_FIRST_CONTACT:
                return self.document.get_worksheet(self.sheet_number).col_values(6)[1:]
            elif column == WorkSheetColumnEnum.RESPONSE_VERIFICATION:
                return self.document.get_worksheet(self.sheet_number).col_values(7)[1:]
            elif column == WorkSheetColumnEnum.WPP_EXISTENCE:
                return self.document.get_worksheet(self.sheet_number).col_values(8)[1:]
        except (WorksheetNotFound, IndexError) as e:
            raise ColumnNotFoundException(
                f'{column.name} column don\'t found. For more details contact support with this error detail: '
                f'{str(e)}'
            )

    def update_column(
            self,
            *,
            column: WorkSheetColumnEnum,
            data_list: list[str | bool | datetime],
            sheet_name: str = None
    ):
        """ """
        try:
            self.sheet_verification(sheet_name=sheet_name if sheet_name else self.sheet_name)
            if column == WorkSheetColumnEnum.PHONES:
                phones: list[str] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.PHONES, [[phone] for phone in phones]
                )
            elif column == WorkSheetColumnEnum.APPROVALS:
                approvals: list[bool] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.APPROVALS, [[approval] for approval in approvals]
                )
            elif column == WorkSheetColumnEnum.SEND_VERIFICATIONS:
                send_verifications: list[bool] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.SEND_VERIFICATIONS,
                    [[send_verification] for send_verification in send_verifications]
                )
            elif column == WorkSheetColumnEnum.DATE_FIRST_CONTACT:
                first_contact_dates: list[datetime] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.DATE_FIRST_CONTACT,
                    [[first_contact_date] for first_contact_date in first_contact_dates]
                )
            elif column == WorkSheetColumnEnum.RESPONSE_VERIFICATION:
                response_verifications: list[bool] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.RESPONSE_VERIFICATION,
                    [[response_verification] for response_verification in response_verifications],
                )
            elif column == WorkSheetColumnEnum.WPP_EXISTENCE:
                wpp_existences: list[bool] = data_list
                self.document.get_worksheet(self.sheet_number).update(
                    WorkSheetColumnEnum.WPP_EXISTENCE, [[wpp_existence] for wpp_existence in wpp_existences]
                )
        except WorksheetNotFound:
            raise ColumnNotFoundException(
                f'Worksheet {self.sheet_name} not found in current document {self.document_name}'
            )
        except ValidationError:
            raise IncorrectTypeException(
                f'Incorrect type of data for column {column.name}'
            )

    def _get_sheets_names(self) -> list[str]:
        """ """
        return [sheet.title for sheet in self.document.worksheets()]

    def _get_cell_value(
            self,
            *,
            row: int,
            col: int,
            sheet_name: str = None
    ):
        """ """
        try:
            self.sheet_verification(sheet_name=sheet_name if sheet_name else self.sheet_name)
            return self.document.get_worksheet(self.sheet_number).cell(row, col).value
        except WorksheetNotFound:
            raise WorksheetNotFound(
                f'Worksheet {self.sheet_name} not found in current document {self.document_name}'
            )

    def _update_sheet_cell(
            self,
            *,
            row: int,
            col: int,
            value: Any,
            sheet_name: str = None
    ):
        """ """
        try:
            self.sheet_verification(sheet_name=sheet_name if sheet_name else self.sheet_name)
            self.document.get_worksheet(self.sheet_number).update_cell(row, col, value)
        except WorksheetNotFound:
            raise WorksheetNotFound(
                f'Worksheet {self.sheet_name} not found in current document {self.document_name}'
            )
