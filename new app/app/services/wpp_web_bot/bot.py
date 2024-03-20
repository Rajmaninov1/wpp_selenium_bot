import phonenumbers

from services.google_sheets.spreadsheets import SpreadSheet
from .wrapper import WppWrapper


class WppBot:
    """
    Uses the spreadsheet to send a message to a list of numbers. The numbers may be in international format, otherwise
    the number will be ignored.
    """
    def __init__(self, spreadsheet_name: str, sheet_name: str):
        self.wpp_wrapper: WppWrapper = WppWrapper()
        self.spreadsheet: SpreadSheet = SpreadSheet(spreadsheet_name, sheet_name)

    def change_sheet(self, new_sheet_name: str):
        self.spreadsheet = SpreadSheet(self.spreadsheet.sheet_name, new_sheet_name)

    @staticmethod
    def phone_verification(phone: str, country_code: str = "CO"):
        try:
            phone = phonenumbers.parse(phone, country_code)
            if phonenumbers.is_valid_number(phone):
                phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
                return True, str(phone)
            return False, str(phone)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False, str(phone)

    def send_messages_to_sheet_numbers(self, message: str, image_path: str = None, country_code: str = "CO"):
        history = {}
        for phone in self.spreadsheet.get_phones_column():
            history[phone] = []
            phone_verification, phone_verified = self.phone_verification(phone, country_code)
            if phone_verification:
                history[phone].append(f"Sending message")
                try:
                    if not self.wpp_wrapper.find_user(phone_verified):
                        history[phone].append(f"Error sending message: User not found")
                        continue
                    if image_path:
                        self.wpp_wrapper.send_picture(image_path, message)
                    else:
                        self.wpp_wrapper.send_message(message)
                    history[phone].append(f"Message sent")
                except Exception as e:
                    history[phone].append(f"Error sending message: {e}")
                    continue
            else:
                history[phone].append(f"Invalid phone number: {phone}")
        self.wpp_wrapper.close_when_message_successfully_sent()
        return history
