import base64
import os
import sys
from time import sleep

from alright import WhatsApp, LOGGER
from fake_http_header import FakeHttpHeader
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class WhatsApp(WhatsApp):
    """
    Selenium Wrapper for WhatsApp Web. Base code and documentation can be found at https://github.com/Kalebu/alright
    """

    def __init__(self, browser=None, time_out=600):
        # CJM - 20220419: Added time_out=600 to allow the call with less than 600 sec timeout
        # web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")

        self.BASE_URL = "https://web.whatsapp.com/"
        self.suffix_link = "https://web.whatsapp.com/send?phone={mobile}&text&type=phone_number&app_absent=1"

        if not browser:
            browser = webdriver.Remote(
                command_executor="http://chrome:4444/wd/hub",
                options=self.chrome_options,
            )
            handles = browser.window_handles
            for x in range(len(handles)):
                if handles[x] != browser.current_window_handle:
                    browser.switch_to.window(handles[x])
                    browser.close()

        self.browser = browser
        self.wait = WebDriverWait(self.browser, time_out)
        self.cli()
        self.login()
        self.mobile = ""

    @property
    def chrome_options(self):
        chrome_options = Options()
        if sys.platform == "win32":
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument(
                f"--user-data-dir={os.path.abspath(os.getcwd())}/private_files/chrome_data/ChromeProfile"
            )
        else:
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--user-data-dir=/home/seluser/chrome_data/UserData")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        fake_header = FakeHttpHeader()
        chrome_options.add_argument(f"--user-agent=User-Agent: {fake_header.user_agent}")
        chrome_options.add_argument(f"--accept-language=Accept-Language: {fake_header.accept_language}")
        chrome_options.add_argument(f"--accept-encoding=Accept-Encoding: {fake_header.accept_encoding}")
        chrome_options.add_argument(f"--accept=Accept: {fake_header.accept}")
        chrome_options.add_argument(f"--referer=Referer: {fake_header.referer}")
        return chrome_options

    def login(self):
        print("Entering login method.")
        _qr_canvas_xpath = "//*[@id='app']/div/div/div[3]/div[1]/div/div[2]/div/canvas"
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()
        print("Waiting for QR code or sidebar to appear.")
        self.wait.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"{_qr_canvas_xpath} | //div[@id='side']")
            )
        )
        print("found side bar or qr code")
        qr_code_canvas = self.browser.find_elements(By.XPATH, _qr_canvas_xpath)
        if len(qr_code_canvas) > 0:
            print("[+] QR code found")
            self.get_qr_code(qr_code_canvas, _qr_canvas_xpath)

    def get_qr_code(self, canvas, _qr_canvas_xpath):
        qr_base64 = self.browser.execute_script(
            "return arguments[0].toDataURL('image/png').substring(22);", canvas[0]
        )
        qr_png = base64.b64decode(qr_base64)
        with open("private_files/qr_codes/qr.png", "wb") as f:
            f.write(qr_png)
        current_qr = self.browser.execute_script(
            "return arguments[0].toDataURL('image/png').substring(22);", canvas[0]
        )
        new_qr = current_qr
        while len(canvas) > 0:
            sleep(5)
            try:
                new_qr = self.browser.execute_script(
                    "return arguments[0].toDataURL('image/png').substring(22);",
                    canvas[0],
                )
            except StaleElementReferenceException as e:
                pass
            if current_qr != new_qr:
                self.get_qr_code(canvas, _qr_canvas_xpath)
            canvas = self.browser.find_elements(By.XPATH, _qr_canvas_xpath)

    def find_user(self, mobile):
        super().find_user(mobile)
        sleep(1)
        not_found_user = self.browser.find_elements(
            By.XPATH, "//*[@id='app']/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div"
        )
        if not_found_user:
            not_found_user[0].click()
            return False
        return True

    def wait_until_message_successfully_sent(self):
        LOGGER.info("Waiting for message status update to continue sending messages...")
        try:
            # Waiting for the pending clock icon to disappear
            sleep(1)
            self.wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"] | //*[@id="main"]//*[@data-icon="msg-dblcheck"] | //*[@id="main"]//*[@data-icon="msg-check"]')
                )
            )
            self.wait.until_not(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]//*[@data-icon="msg-time"]')
                )
            )
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")

    def close_when_message_successfully_sent(self):
        self.wait_until_message_successfully_sent()
        LOGGER.info("Messages sent successfully. Closing browser...")
        self.browser.close()

    def send_message(self, message):
        super().send_message(message)
        self.wait_until_message_successfully_sent()

    def send_picture(self, picture, message):
        super().send_picture(picture, message)
        self.wait_until_message_successfully_sent()
