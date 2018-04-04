import sys

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import ConnectionError

EXT_ID = "nfjcdbackpnnlbnkmjfjgiokldjefbma"

class SeleniumScraper:
    headers = {}
    HEADERS_TO_LOG = ["x-frame-options", "content-security-policy"]

    def __init__(self, chromedriver, width=None, height=None, user_agent=None):
        opts = Options()
        opts.set_headless(True)
        if width and height:
            opts.add_argument("--window-size={},{}".format(width, height))

        if user_agent:
            opts.add_argument("user-agent={}".format(user_agent))
        #opts.binary_location = "/usr/bin/google-chrome-stable"

        opts.add_argument("load-extension=chrome_ext")
        opts.add_argument("load-extension-key=chrome_ext.pem")

        self.driver = webdriver.Chrome(chromedriver, options=opts)
        if user_agent:
            print("Chrome Headless Browser Invoked with Custom User Agent")
        else:
            print("Chrome Headless Browser Invoked")

    def analyze(self, url):
        self.driver.get(url)
        mobile_url = self.driver.current_url
        if mobile_url != url:
            print("Redirect to " + mobile_url)

        self.driver.get("chrome-extension://{}/_generated_background_page.html".format(EXT_ID))

        return self.driver.execute_async_script(
            "chrome.storage.local.get('securityHeaders', arguments[0])")

    def shutdown(self):
        self.driver.quit()
