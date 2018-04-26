import sys
import os

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *

from config import *

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
EMPTY_HTML_PATH = os.path.join(__location__, "empty.html")

class frame_JS_to_be_available_and_switch_to_it:  # Default: check every 500 ms
    def __init__(self, locator):
        self.locator = locator
    def __call__(self, driver):
        try:
            driver.switch_to.frame(self.locator)
        except NoSuchFrameException:
            return False
        return not driver.execute_script('return self === top')

class SeleniumScraper:
    headers = {}
    HEADERS_TO_LOG = ["x-frame-options", "content-security-policy"]

    def __init__(self,
                 chromedriver,
                 width=None,
                 height=None,
                 user_agent=None,
                 extensions=[]):
        opts = Options()
        if width and height:
            opts.add_argument("--window-size={},{}".format(width, height))

        if user_agent:
            opts.add_argument("user-agent={}".format(user_agent))
        #opts.binary_location = "/usr/bin/google-chrome-stable"

        if extensions:
            for ext in extensions:
                opts.add_argument("load-extension={}".format(ext))

        self.driver = webdriver.Chrome(chromedriver, options=opts)
        if user_agent:
            print("Chrome Headless Browser Invoked with Custom User Agent")
        else:
            print("Chrome Headless Browser Invoked")

    def frame_test(self, url, fpath):
        # FIXME: find a way to get a full screenshot without resizing the window?
        #self.driver.set_window_rect(width=1920, height=1080)
        self.driver.get("file://{}".format(EMPTY_HTML_PATH))
        newframe_js = " ".join([
            'var newframe = document.createElement("iframe");',
            'newframe.id = "myframe";',
            'newframe.height = screen.height;',
            'newframe.width = screen.width;',
            'newframe.src = "{}";'.format(url),
            'document.body.appendChild(newframe)'
        ])
        print newframe_js
        self.driver.execute_script(newframe_js)
        WebDriverWait(self.driver, FRAME_LOAD_WAIT).until(frame_JS_to_be_available_and_switch_to_it("myframe"))
        self.driver.save_screenshot(fpath)

    def get_security_headers(self, url):
        # FIXME: reset window size for mobile test
        self.driver.get(url)
        mobile_url = self.driver.current_url
        if mobile_url != url:
            print("Redirect to " + mobile_url)

        self.driver.get("chrome-extension://{}/_generated_background_page.html".format(EXT_ID))

        return self.driver.execute_async_script(
            "chrome.storage.local.get('securityHeaders', arguments[0])")['securityHeaders']

    def shutdown(self):
        self.driver.quit()
