import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumScraper:
    headers = {}
    HEADERS_TO_LOG = ["X-Frame-Options", "Content-Security-Policy"]

    def __init__(self, chromedriver, width, height, user_agent):
        self.request_headers = {'user-agent': user_agent}

        opts = Options()
        opts.set_headless(True)
        opts.add_argument("--window-size={},{}".format(width, height))
        opts.add_argument("user-agent={}".format(user_agent))
        #opts.binary_location = "/usr/bin/google-chrome-stable"

        self.driver = webdriver.Chrome(chromedriver, options=opts)
        print("Chrome Headless Browser Invoked")

    def analyze(self, url):
        self.driver.get(url)
        mobile_url = self.driver.current_url
        if mobile_url != url:
            print("Mobile redirect to " + mobile_url)

        r = requests.get(mobile_url, headers=self.request_headers)
        self.headers[url] = dict(
            ((k, v) for (k, v) in r.headers.iteritems()
             if k in self.HEADERS_TO_LOG))

    def shutdown(self):
        self.driver.quit()
