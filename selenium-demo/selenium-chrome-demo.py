import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, "chromedriver")

WINDOW_WIDTH = 366
WINDOW_HEIGHT = 626
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"

opts = Options()
opts.set_headless(True)
opts.add_argument("--window-size={},{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
opts.add_argument("user-agent={}".format(USER_AGENT))
#opts.binary_location = "/usr/bin/google-chrome-stable"

driver = webdriver.Chrome(CHROME_PATH, options=opts)
print("Chrome Headless Browser Invoked")
driver.get("https://youtube.com")
print(driver.current_url)
driver.quit()
