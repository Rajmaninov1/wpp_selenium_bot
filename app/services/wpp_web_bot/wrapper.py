import base64
import os
import sys
from pathlib import Path

from alright import WhatsApp, LOGGER
from fake_http_header import FakeHttpHeader
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from config.settings import settings, Environment
from schemas.wpp_web_bot.html_wpp_identifiers import HtmlWppXpaths, JavaScriptWppScripts
from schemas.wpp_web_bot.media_types import MediaTypesEnum

if not settings.REMOTE_BROWSER:
    from webdriver_manager.chrome import ChromeDriverManager


class WppWrapper(WhatsApp):
    """
    Selenium Wrapper for WhatsApp Web. Base code and documentation can be found at https://github.com/Kalebu/alright
    """
    def __init__(self, browser: WebDriver | None = None, time_out: int = 90):  # noqa
        # web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")

        self.browser_open = True
        self.BASE_URL: str = 'https://web.whatsapp.com/'
        self.suffix_link: str = 'https://web.whatsapp.com/send?phone={mobile}&text&type=phone_number&app_absent=1'

        if not browser:
            if settings.REMOTE_BROWSER:
                browser = webdriver.Remote(
                    command_executor='http://chrome:4444/wd/hub',
                    options=self.chrome_options,
                )
            else:
                browser = webdriver.Chrome(
                    ChromeDriverManager().install(),
                    options=self.chrome_options,
                )
            handles = browser.window_handles
            for x in range(len(handles)):
                if handles[x] != browser.current_window_handle:
                    browser.switch_to.window(handles[x])
                    browser.close()

        self.browser: WebDriver = browser
        self.wait: WebDriverWait = WebDriverWait(self.browser, time_out)
        self.cli()
        self.mobile = ''
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    @property
    def chrome_options(self) -> Options:
        chrome_options: Options = Options()
        if sys.platform == 'win32':
            chrome_options.add_argument('--profile-directory=ChromeProfile')
            chrome_options.add_argument(
                f'--user-data-dir={os.path.abspath(os.getcwd())}/files/chrome_data/ChromeProfile')
        else:
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--user-data-dir=/home/seluser/chrome_data/UserData')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option(
            'prefs', {'profile.managed_default_content_settings.images': 2})
        chrome_options.add_argument('--no-sandbox')  # EVALUATE IF SECURITY RISK IS MORE THAN THE RESOURCES SAVED
        if settings.ENVIRONMENT != Environment.DEV:
            chrome_options.add_argument('--headless')
        # add fake headers
        fake_header = self._generate_new_headers()
        chrome_options.add_argument(f'--user-agent=User-Agent: {fake_header.user_agent}')
        chrome_options.add_argument(f'--accept-language=Accept-Language: {fake_header.accept_language}')
        chrome_options.add_argument(f'--accept-encoding=Accept-Encoding: {fake_header.accept_encoding}')
        chrome_options.add_argument(f'--accept=Accept: {fake_header.accept}')
        chrome_options.add_argument(f'--referer=Referer: {fake_header.referer}')
        return chrome_options

    def login(self) -> bytes | None:
        print('Entering login method.')
        _qr_canvas_xpath: HtmlWppXpaths = HtmlWppXpaths.QR_CANVAS_XPATH
        print('Waiting for QR code or sidebar to appear.')
        self.wait.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, HtmlWppXpaths.QR_CANVAS_OR_SIDE_PANEL_XPATH)
            )
        )
        print('found side bar or qr code')
        qr_code_canvas: list[WebElement] = self.browser.find_elements(By.XPATH, _qr_canvas_xpath)
        if len(qr_code_canvas) > 0:
            print('[+] QR code found')
            return self.get_qr_code(qr_code_canvas, _qr_canvas_xpath)
        else:
            return None

    def get_qr_code(self, canvas: list[WebElement], _qr_canvas_xpath: HtmlWppXpaths) -> bytes:
        qr_base64: str = self.browser.execute_script(
            JavaScriptWppScripts.GET_QR_IMG, canvas[0]
        )
        qr_png: bytes | None = base64.b64decode(qr_base64)
        if qr_png:
            return qr_png
        current_qr: str = self.browser.execute_script(
            JavaScriptWppScripts.GET_QR_IMG, canvas[0]
        )
        new_qr: str = current_qr
        while len(canvas) > 0:
            try:
                new_qr: str = self.browser.execute_script(
                    JavaScriptWppScripts.GET_QR_IMG,
                    canvas[0],
                )
            except StaleElementReferenceException:
                pass
            if current_qr != new_qr:
                self.get_qr_code(canvas, _qr_canvas_xpath)
            canvas: list[WebElement] = self.browser.find_elements(By.XPATH, _qr_canvas_xpath)

    def find_user(self, mobile):
        super().find_user(mobile)
        not_found_user: list[WebElement] = self.browser.find_elements(
            By.XPATH,
            HtmlWppXpaths.NOT_FOUND_USER_NOTIFICATION_XPATH
        )
        if not_found_user:
            not_found_user[0].click()
            return False
        return True

    def wait_until_message_successfully_sent(self):
        LOGGER.info('Waiting for message status update to continue sending messages...')
        try:
            # Waiting for the pending clock icon to disappear
            self.wait.until(
                expected_conditions.presence_of_element_located((
                    By.XPATH,
                    HtmlWppXpaths.CLOCK_OR_CHECK_OR_DOUBLE_CHECK_MESSAGE_STATE_XPATH
                ))
            )
            self.wait.until_not(
                expected_conditions.presence_of_element_located((
                    By.XPATH,
                    HtmlWppXpaths.CLOCK_MESSAGE_STATE_XPATH
                ))
            )
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f'Failed to send a message to {self.mobile} - {bug}')

    def close_when_message_successfully_sent(self):
        self.wait_until_message_successfully_sent()
        LOGGER.info('Messages sent successfully. Closing browser...')
        self.browser.quit()

    def send_message(self, message: str, timeout=0.0):
        super().send_message(message)
        self.wait_until_message_successfully_sent()

    def send_picture(self, picture: Path, message: str | None = None):
        try:
            filename = os.path.realpath(picture)
            self.find_attachment()
            # To send an Image
            img_button = self.wait.until(
                expected_conditions.presence_of_element_located(
                    (
                        By.XPATH,
                        HtmlWppXpaths.IMG_INPUT_BUTTON_XPATH,
                    )
                )
            )
            img_button.send_keys(filename)
            if message:
                self.add_caption(message, media_type=MediaTypesEnum.IMAGE)
            self.send_attachment()
            LOGGER.info(f"Picture has been successfully sent to {self.mobile}")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_picture() finished running!")
        self.wait_until_message_successfully_sent()

    def send_video(self, video: Path, message: str | None = None):
        try:
            filename = os.path.realpath(video)
            f_size = os.path.getsize(filename)
            x = self.convert_bytes_to(f_size, "MB")
            if x < 14:
                # File is less than 14MB
                self.find_attachment()
                # To send a Video
                video_button = self.wait.until(
                    expected_conditions.presence_of_element_located(
                        (
                            By.XPATH,
                            HtmlWppXpaths.VID_INPUT_BUTTON_XPATH,
                        )
                    )
                )

                video_button.send_keys(filename)
                if message:
                    self.add_caption(message, media_type=MediaTypesEnum.VIDEO)
                self.send_attachment()
                LOGGER.info(f"Video has been successfully sent to {self.mobile}")
            else:
                LOGGER.info(f"Video larger than 14MB")
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a message to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_video() finished running!")
        self.wait_until_message_successfully_sent()

    def send_file(self, filename: Path, message: str | None = None):
        try:
            filename = os.path.realpath(filename)
            self.find_attachment()
            document_button = self.wait.until(
                expected_conditions.presence_of_element_located(
                    (
                        By.XPATH,
                        HtmlWppXpaths.DOC_INPUT_BUTTON_XPATH,
                    )
                )
            )
            document_button.send_keys(filename)
            if message:
                self.add_caption(message, media_type=MediaTypesEnum.FILE)
            self.send_attachment()
        except (NoSuchElementException, Exception) as bug:
            LOGGER.exception(f"Failed to send a file to {self.mobile} - {bug}")
        finally:
            LOGGER.info("send_file() finished running!")
        self.wait_until_message_successfully_sent()

    def add_caption(self, message: str, media_type: MediaTypesEnum = MediaTypesEnum.IMAGE):
        xpath_map = {
            MediaTypesEnum.IMAGE: HtmlWppXpaths.IMG_CAPTION_XPATH,
            MediaTypesEnum.VIDEO: HtmlWppXpaths.VID_CAPTION_XPATH,
            MediaTypesEnum.FILE: HtmlWppXpaths.DOC_CAPTION_XPATH,
        }
        self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, HtmlWppXpaths.FILE_CANVA_XPATH))
        )
        ActionChains(self.browser).key_down(Keys.TAB).key_up(Keys.TAB).perform()
        input_box = self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath_map[media_type]))
        )
        for line in message.split("\n"):
            input_box.send_keys(line)
            ActionChains(self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()  # noqa

    def send_attachment(self):
        # Waiting for the pending clock icon to disappear
        self.wait.until_not(
            expected_conditions.presence_of_element_located(
                (By.XPATH, HtmlWppXpaths.CLOCK_MESSAGE_STATE_XPATH)
            )
        )

        send_button = self.wait.until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    HtmlWppXpaths.SEND_BUTTON_XPATH,
                )
            )
        )
        send_button.click()

        # Waiting for the pending clock icon to disappear again - workaround for large files or loading videos.
        # Appropriate solution for the presented issue. [nCKbr]
        self.wait.until_not(
            expected_conditions.presence_of_element_located(
                (By.XPATH, HtmlWppXpaths.CLOCK_MESSAGE_STATE_XPATH)
            )
        )

    @staticmethod
    def _generate_new_headers() -> FakeHttpHeader:
        """
        FakeHttpHeader has error when in COUNTRY_TOP_LEVEL_DOMAINS random choice
        chooses eu, so retry in that case until it works selecting other value
        """
        while True:
            try:
                return FakeHttpHeader(browser='chrome')
            except KeyError:
                pass


wpp_wrapper: WppWrapper = WppWrapper()
