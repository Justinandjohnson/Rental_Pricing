# Data Basics
import pandas as pd
import numpy as np
from datetime import datetime as dt

pd.options.display.float_format = "{:.0f}".format

# scraping
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# to install ChromeDriverManager() on first use
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.addArguments("--no-sandbox");
# chrome_options.add_arguments("--disable-dev-shm-usage")
# webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# webdriver.Chrome(ChromeDriverManager().install())


import time
import requests
from tqdm import tqdm
import os


class SiteReader:
    def __init__(self):
        """ Headless options for script """
        chrome_options = Options()
        # Comment out when developing / debugging
        chrome_options.add_argument("--no-sandbox")
        # # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=800,600")
        chrome_options.add_argument("--remote-debugging-port=9222")
        print(f"Chrome headless is set to: {chrome_options.headless}")
        # self.driver = webdriver.Chrome(options=chrome_options)

        # Prototyping
        self.driver = webdriver.Chrome()

        # if webdriver gets stuck in headless mode, webdriver.ChromeOptions.set_headless=False
        base_url = "https://www.trulia.com"
        page_url = "/for_rent/Austin,TX/"


def main():
    """ MAIN """


if __name__ == "__main__":
    main()

    print(f"Starting...")
    os.system(
        "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0"
    )
    os.system("echo $DISPLAY")
    bot = SiteReader()
