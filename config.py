import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_webdriver():
    """
    Sets up the webdriver according to where the chromedriver is on the PATH.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    if sys.platform in ['linux', 'darwin']:
        return webdriver.Chrome(options=chrome_options)
    else:
        return webdriver.Chrome('C:/Program Files/chromedriver_win32/chromedriver.exe',
                                options=chrome_options)
