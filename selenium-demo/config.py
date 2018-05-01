INPUT_DOMAINS = "top-1m.txt"
SCREENSHOTS_DIR = "screenshots"
HEADERS_DIR = "headers"

MOBILE_WIDTH = 370
MOBILE_HEIGHT = 685
#MOBILE_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
MOBILE_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36"

USE_XVFB = True
RUN_DESKTOP_TEST = True
RUN_MOBILE_TEST = True

DEBUG = True
DEBUG_LIMIT = 1000

DOMAIN_START = 391

EXT_ID = "nfjcdbackpnnlbnkmjfjgiokldjefbma"

PAGE_LOAD_TIMEOUT = 10  # seconds
FRAME_LOAD_WAIT = 10  # seconds

def GET_OUTPUT_FNAME():
    from time import strftime
    from os import makedirs
    from os.path import join
    from errno import EEXIST
    try:
        makedirs(HEADERS_DIR)
    except OSError as e:
        if e.errno != EEXIST:
            raise
    return strftime(join(HEADERS_DIR, "%Y-%m-%d_%H:%M:%S.csv"))
