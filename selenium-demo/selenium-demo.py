import os

from SeleniumScraper import SeleniumScraper

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, "chromedriver")

WINDOW_WIDTH = 366
WINDOW_HEIGHT = 626
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"

scraper = SeleniumScraper(CHROME_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, USER_AGENT)
scraper.analyze("http://taobao.com")
print(scraper.headers)
