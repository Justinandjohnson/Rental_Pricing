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


class SiteReader:
    def __init__(self):
        """ Headless options for script """
        chrome_options = Options()
        # Comment out when developing / debugging
        chrome_options.add_argument("--no-sandbox")
        # # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=800,600")
        chrome_options.add_argument("--remote-debugging-port=9222")
        print(chrome_options.headless)
        # self.driver = webdriver.Chrome(options=chrome_options)

        # Prototyping
        self.driver = webdriver.Chrome()

        # if webdriver gets stuck in headless mode, webdriver.ChromeOptions.set_headless=False

    def get_url_list(self):
        """Gets a list of urls from main page to scrape."""
        # self.driver.get(
        #     "https://www.trulia.com/for_rent/Austin,TX/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/"
        # )\

        url_list = []
        last_page = False
        base_url = "https://www.trulia.com"
        page_url = "/for_rent/Austin,TX/"
        i = 1
        while last_page == False and i < 100:
            # for i in range(98):
            time.sleep(3)
            self.driver.get(base_url + page_url)
            html = self.driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(html, features="lxml")

            for div in soup.find_all(
                "div",
                {
                    "data-hero-element-id": "srp-home-card",
                    "data-hero-element-id": "false",
                },
            ):
                # print(div)
                url = div.find("a").attrs["href"]
                url_list.append(url)

            # check if last page and exit while loop
            if soup.find("a", {"aria-label": "Next Page"}):
                last_page = False
                page_url = soup.find("a", {"aria-label": "Next Page"})["href"]
                print(page_url)
                time.sleep(10)
            else:
                last_page = True
            # print(url_list)

            # keep this up, if recapcha fails this errors out so you can fix it,
            # headless=False in this senario of course...
            print(f"Page: {i} last listing: {url_list[-1]}")
            i += 1
        return url_list


def main():
    """ MAIN """
    bot = SiteReader()
    ulist = bot.get_url_list()
    to_save = pd.DataFrame(ulist)
    to_save.to_csv("current_listings.csv")


if __name__ == "__main__":
    main()
