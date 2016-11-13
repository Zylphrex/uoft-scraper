import dryscrape
import sys


########################################
# variables go here
_session = None
########################################

def set_up():
    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()


def start_session(url):
    global _session

    # set up a web scraping session
    _session = dryscrape.Session(base_url = url)

    # don't need images
    _session.set_attribute('auto_load_images', False)

    # begin session at home page
    home()


def home():
    global _session
    # return to home page
    _session.visit('/')

def at_xpath(xpath):
    return _session.at_xpath(xpath)
