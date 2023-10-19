import os
import re
import sys
from time import sleep

from bs4 import BeautifulSoup
from fake_http_header import FakeHttpHeader
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class GoogleMaps:
    """Google Maps Web Wrapper"""

    def __init__(self, browser=None, time_out=600):

        self.BASE_URL = "https://www.google.com/search?sxsrf=AOaemvJFlZpUo_x9-cto6m55dikbhPjYEg:\
                1640914337240&q=0&rflfq=1&rldoc=1&rllag=4756802,-74199411,6658&tbm=lcl&sa=\
                X&ved=2ahUKEwif-rWh8oz1AhWeSTABHZqmCCYQtgN6BAgCEFM&biw=1920&bih=1011&dpr=\
                1&fll=0,0&fspn=0.33010749999999955,0.20458689999999535&fz=0&sll=0,0&sspn=\
                0.33010749999999955,0.20458689999999535&sz=0&tbs=lrf:!1m4!1u3!2m2!3m1!1e1\
                !1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2&rlst=f#rlfi=hd:;si\
                :;mv:[];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3\
                sIAE,lf:1,lf_ui:2"
        self.input_bar_xpath = '//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input'
        self.side_bar_xpath = '//*[@id="res"]/div'
        self.list_of_elements_xpath = '//*[@id="rl_ist0"]/div/div[1]'

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
        self.browser.get(self.BASE_URL)
        self.browser.maximize_window()

    def search(self, search_text):
        try:
            search_box = self.wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, self.input_bar_xpath)
                )
            )
            search_box.send_keys(search_text)
            search_box.submit()
            sleep(1)
        except Exception:
            sleep(1)
            self.search(search_text)

    def get_search_results(self):
        scrapped_data = {}
        page = 0
        elements_inside_res_element = len(self.browser.find_elements(By.XPATH, self.side_bar_xpath))
        while True:
            page += 1
            print(f"Page: {page}")
            while len(self.browser.find_elements(By.XPATH, self.side_bar_xpath)) > elements_inside_res_element:
                sleep(0.5)
            html = self.wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, self.list_of_elements_xpath)
                )
            ).get_attribute('innerHTML')
            soup = BeautifulSoup(html, "html.parser")
            for result in soup.find_all("div", class_="VkpGBb"):
                try:
                    name = result.find("div", class_="dbg0pd").text
                except (AttributeError, TypeError):
                    name = None
                try:
                    score = result.find("span", class_="YDIN4c YrbPuc").text
                    number_of_opinions = "".join(filter(str.isdigit, result.find("span", class_="HypWnf YrbPuc").text))
                except (AttributeError, TypeError):
                    score = None
                    number_of_opinions = None
                try:
                    # TODO get phone number in result.find("div", class_="rllt__details").text
                    phone_number = re.search("[\d ]{7,}", result.find("div", class_="rllt__details").text)[0].replace(" ", "")
                except (AttributeError, TypeError):
                    phone_number = None
                try:
                    website = result.find("a", href=True)["href"]
                    website = website if website != "#" else None
                except (AttributeError, TypeError):
                    website = None

                scrapped_data[name] = {
                    "name": name,
                    "score": score,
                    "number_of_opinions": number_of_opinions,
                    "phone_number": phone_number,
                    "website": website,
                }
            print("number of scrapped_data: ", len(scrapped_data))
            sleep(1.5)
            try:
                self.browser.find_element(By.ID, "pnnext").click()
            except NoSuchElementException:
                break
        return scrapped_data

    def search_in_landing(self, scrapped_data):
        for business in scrapped_data:
            scrapped_data[business]["email"] = None
            if scrapped_data[business]["website"]:
                try:
                    self.browser.get(scrapped_data[business]["website"])
                    html = self.browser.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
                    email = re.findall(r"[\w.-]+@[\w.-]+", html)
                    if email:
                        scrapped_data[business]["email"] = email[-1]

                except Exception as e:
                    print("Error in website:", e)
        return scrapped_data

    def close_session(self):
        self.browser.quit()
