import gspread
from google.oauth2.service_account import Credentials


def open_document(document_name: str):
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

    def __init__(self, document, sheet_name):
        self.document = document
        self.sheet_name = sheet_name
        self.sheets = open_document(self.document)
        self.sheet_number = self.get_sheets_names().index(sheet_name)

    def sheet_verification(self, sheet_name):
        """ """
        if sheet_name is not None:
            sheets_names = self.get_sheets_names()
            if sheet_name in sheets_names:
                self.sheet_name = sheet_name
                self.sheet_number = sheets_names.index(sheet_name)
            else:
                pass

    def get_sheets_names(self):
        """ """
        return [row.title for row in self.sheets.worksheets()]

    def get_phones_column(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(3)[1:]

    def get_approval_column(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(4)[1:]

    def get_send_verification_column(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(5)[1:]

    def get_first_contact_date_colum(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(6)[1:]

    def get_response_verification_column(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(7)[1:]

    def get_wpp_existence_column(self, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).col_values(8)[1:]

    def get_cell_value(self, row, col, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        return self.sheets.get_worksheet(self.sheet_number).cell(row, col).value

    def update_phones_column(self, phones, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "C2:C", [[phone] for phone in phones]
        )

    def update_approval_column(self, approvals, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "D2:D", [[approval] for approval in approvals]
        )

    def update_send_verification_column(self, send_verifications, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "E2:E", [[send_verification] for send_verification in send_verifications]
        )

    def update_first_contact_date_column(self, first_contact_dates, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "F2:F", [[first_contact_date] for first_contact_date in first_contact_dates]
        )

    def update_response_verification_column(
            self, response_verifications, sheet_name=None
    ):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "G2:G",
            [
                [response_verification]
                for response_verification in response_verifications
            ],
        )

    def update_wpp_existence_column(self, wpp_existences, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update(
            "H2:H", [[wpp_existence] for wpp_existence in wpp_existences]
        )

    def update_sheet_cell(self, row, col, value, sheet_name=None):
        """ """
        self.sheet_verification(sheet_name)
        self.sheets.get_worksheet(self.sheet_number).update_cell(row, col, value)  # actualizar línea
