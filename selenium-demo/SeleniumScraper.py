import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumScraper:
    headers = {}
    HEADERS_TO_LOG = ["X-Frame-Options", "Content-Security-Policy"]
    request_headers = None

    def __init__(self, chromedriver, width=None, height=None, user_agent=None):
        if user_agent:
            self.request_headers = {'user-agent': user_agent}

        opts = Options()
        opts.set_headless(True)
        if width and height:
            opts.add_argument("--window-size={},{}".format(width, height))

        if user_agent:
            opts.add_argument("user-agent={}".format(user_agent))
        #opts.binary_location = "/usr/bin/google-chrome-stable"

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

        r = requests.get(mobile_url, headers=self.request_headers)
        return dict(((k, v) for (k, v) in r.headers.iteritems()
                     if k in self.HEADERS_TO_LOG))

    def shutdown(self):
        self.driver.quit()