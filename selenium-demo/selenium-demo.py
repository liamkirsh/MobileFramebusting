#!/usr/bin/env python
import os
import sys
import subprocess
import csv
import errno


from SeleniumScraper import SeleniumScraper
from config import *

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, "chromedriver")

if len(sys.argv) > 1:
	INPUT_DOMAINS = sys.argv[1];

def check_setup():
    # Try to find Chrome 64 installation
    browser_exes = ["google-chrome", "chrome", "google-chrome-stable"]
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
        os.makedirs(SCREENSHOTS_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def has_framebust_header(security_headers):
    # FIXME: this is probably incomplete
    # FIXME: consider cases where XFO takes precedent over CSP or vice versa
    def is_framebust_header(header):
        hname = header['name'].lower()
        hvalue = header['value'].lower()

        if hname == 'x-frame-options':
            if (hvalue == 'sameorigin' or
                hvalue == 'deny'):
                return True
        elif hname == 'content-security-policy':
            csp_directives = [directive.strip() for directive in hvalue.split(';')]
            frame_ancestors = next((directive for directive in csp_directives
                                   if directive.startswith("frame-ancestors")), None)
            if frame_ancestors:
                frame_ancestor_sources = frame_ancestors.split()[1:]
                if "'self'" or "'none'" in frame_ancestor_sources:
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
        writer.writerow(['domain', 'desktop xfo', 'desktop csp', 'mobile xfo', 'mobile csp'])
        for rank, domain in enumerate(domains):
            if DEBUG and rank == DEBUG_LIMIT:
                break

            url = "http://" + domain.strip()
            if DEBUG:
                print("Rank {}: checking headers at {}".format(rank, url))

            # Scan desktop
            if RUN_DESKTOP_TEST:
                desktop_headers = desktop_scraper.get_security_headers(url)
                desktop_xfo = next((header['value'] for header in desktop_headers
                                    if header['name'].lower() == 'x-frame-options'), "")
                desktop_csp = next((header['value'] for header in desktop_headers
                                    if header['name'].lower() == 'content-security-policy'), "")
            else:
                desktop_xfo = None
                desktop_csp = None

            # Scan mobile
            if RUN_MOBILE_TEST:
                mobile_headers = mobile_scraper.get_security_headers(url) if TEST_MOBILE else None
                print mobile_headers
                mobile_xfo = next((header['value'] for header in mobile_headers
                                    if header['name'].lower() == 'x-frame-options'), "")
                mobile_csp = next((header['value'] for header in mobile_headers
                                    if header['name'].lower() == 'content-security-policy'), "")
            else:
                mobile_xfo = None
                mobile_csp = None

            writer.writerow([url, desktop_xfo, desktop_csp, mobile_xfo, mobile_csp])
            output.flush()

            if RUN_DESKTOP_TEST:  # and not has_framebust_header(desktop_headers['securityHeaders']):
                fmted_domain = domain.rsplit('.', 1)[0]
                fpath = "{}/{}.png".format(SCREENSHOTS_DIR, fmted_domain)
                desktop_scraper.frame_test(url, fpath)
            if RUN_MOBILE_TEST:   # and not has_framebust_header(mobile_headers['securityHeaders']):
                fmted_domain = domain.rsplit('.', 1)[0]
                fpath = "{}/mobile_{}.png".format(SCREENSHOTS_DIR, fmted_domain)
                mobile_scraper.frame_test(url, fpath)


# https://stackoverflow.com/a/27806978
class dummy_context_mgr():
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def main():
    with Xvfb() if USE_XVFB else dummy_context_mgr() as xvfb:
        desktop_scraper = SeleniumScraper(CHROME_PATH, extensions=["chrome_ext"]) if RUN_DESKTOP_TEST else None
        mobile_scraper = (SeleniumScraper(CHROME_PATH,
                                          width=WINDOW_WIDTH,
                                          height=WINDOW_HEIGHT,
                                          user_agent=USER_AGENT,
                                          extensions=["chrome_ext"])
                          if RUN_MOBILE_TEST else None)

        check_setup()
        crawl_domains(desktop_scraper, mobile_scraper)

if __name__ == "__main__":
    main()
