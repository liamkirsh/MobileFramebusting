#!/usr/bin/env python
import os
import sys
import subprocess
import csv
import errno

from xvfbwrapper import Xvfb

from SeleniumScraper import SeleniumScraper

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, "chromedriver")

INPUT_DOMAINS = "top-100.txt"
OUTPUT_FILE = "headers.csv"

WINDOW_WIDTH = 366
WINDOW_HEIGHT = 626
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"

USE_XVFB = False
TEST_DESKTOP = True
TEST_MOBILE = False

DEBUG = True
if (DEBUG):
    LIMIT = 10
else:
    LIMIT = None


def check_setup():
    # Try to find Chrome 64 installation
    browser_exes = ["google-chrome", "chrome"]
    for browser_exe in browser_exes:
        try:
            proc = subprocess.Popen([browser_exe, "--version"],
                                    stdout=subprocess.PIPE)
        except OSError:
            proc = None
        else:
            if proc.communicate()[0].startswith("Google Chrome 64.0.3282.140"):
                break
            else:
                proc = None
    if not proc:
        sys.stderr.write("Couldn't find Google Chrome 64.0.3282.140\n")
        sys.exit(1)
    if not os.path.isfile("chrome_ext.crx"):
        sys.stderr.write("Couldn't find packaged chrome extension\n")
        sys.exit(1)
    if not os.path.isfile("chrome_ext.pem"):
        sys.stderr.write("Couldn't find chrome extension key\n")
        sys.exit(1)
    # Create screenshots directory if it doesn't exist
    try:
        os.makedirs("screenshots")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def has_framebust_header(security_headers):
    # FIXME: this is probably incomplete
    def is_framebust_header(header):
        if header['name'].lower() == 'x-frame-options':
            if (header['value'].lower() == 'sameorigin' or
                header['value'].lower() == 'deny'):
                return True
        return False

    return any(is_framebust_header(header) for header in security_headers)


def crawl_domains(desktop_scraper, mobile_scraper):
    try:
        domains = open(INPUT_DOMAINS, 'r')
    except IOError:
        sys.stderr.write("Error opening input domain list at " +
                         INPUT_DOMAINS + "\n")
        sys.exit(1)

    with open(OUTPUT_FILE, 'w') as output:
        writer = csv.writer(output)
        writer.writerow(['domain', 'desktop', 'mobile'])
        for rank, domain in enumerate(domains):
            if DEBUG and rank == LIMIT:
                break

            url = "http://" + domain.strip()
            if DEBUG:
                print("Rank {}: checking headers at {}".format(rank, url))

            # Scan desktop
            desktop_headers = desktop_scraper.get_security_headers(url) if TEST_DESKTOP else None

            # Scan mobile
            mobile_headers = mobile_scraper.get_security_headers(url) if TEST_MOBILE else None
            writer.writerow([url, desktop_headers, mobile_headers])
            output.flush()

            if TEST_DESKTOP and not has_framebust_header(desktop_headers['securityHeaders']):
                fmted_domain = domain.rsplit('.', 1)[0]
                fpath = "screenshots/{}.png".format(fmted_domain)
                desktop_scraper.frame_test(url, fpath)
            if TEST_MOBILE and no_framebust_headers(mobile_headers['securityHeaders']):
                fmted_domain = domain.rsplit('.', 1)[0]
                fpath = "screenshots/mobile_{}.png".format(fmted_domain)
                mobile_scraper.frame_test(url, fpath)


# https://stackoverflow.com/a/27806978
class dummy_context_mgr():
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def main():
    with Xvfb() if USE_XVFB else dummy_context_mgr() as xvfb:
        desktop_scraper = SeleniumScraper(CHROME_PATH) if TEST_DESKTOP else None
        mobile_scraper = (SeleniumScraper(CHROME_PATH,
                                          width=WINDOW_WIDTH,
                                          height=WINDOW_HEIGHT,
                                          user_agent=USER_AGENT)
                          if TEST_MOBILE else None)

        check_setup()
        crawl_domains(desktop_scraper, mobile_scraper)

if __name__ == "__main__":
    main()
