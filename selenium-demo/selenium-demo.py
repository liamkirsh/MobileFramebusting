import os
import sys

import csv

from SeleniumScraper import SeleniumScraper

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, "chromedriver")

INPUT_DOMAINS = "top-100.txt"
OUTPUT_FILE = "headers.csv"

WINDOW_WIDTH = 366
WINDOW_HEIGHT = 626
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"

desktop_scraper = SeleniumScraper(CHROME_PATH)
mobile_scraper = SeleniumScraper(CHROME_PATH, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, user_agent=USER_AGENT)

DEBUG = True

if (DEBUG):
    LIMIT = 5  # set to None when not testing
else:
    LIMIT = None

try:
    domains = open(INPUT_DOMAINS, 'r')
except IOError:
    sys.stderr.write("Error opening input domain list at " + INPUT_DOMAINS)
    sys.exit(1)

with open(OUTPUT_FILE, 'w') as output:
    writer = csv.writer(output)
    writer.writerow(['domain','desktop','mobile'])
    for rank, domain in enumerate(domains):
        if DEBUG and rank == LIMIT:
            break

        url = "http://" + domain.strip()
        if DEBUG:
            print("Rank {}: checking headers at {}".format(rank, url))

        # Scan desktop
        desktop_headers = desktop_scraper.analyze(url)
        # Scan mobile
        mobile_headers = mobile_scraper.analyze(url)
        writer.writerow([url, desktop_headers, mobile_headers])

