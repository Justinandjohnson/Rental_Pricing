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

    def get_url_list(self):
        """Gets a list of urls from main page to scrape."""
        # self.driver.get(
        #     "https://www.trulia.com/for_rent/Austin,TX/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/"
        # )\

        url_list = []
        last_page = False
        i = 1
        base_url = "https://www.trulia.com"
        page_url = "/for_rent/Austin,TX/"
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

    def get_apartment_data(self, base_url, current_url):
        """Gets apartment data for the url specified"""
        try:

            time.sleep(0.1)
            # print(base_url + current_url)
            response = self.driver.get(base_url + current_url)
            html = self.driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(html, "lxml")
            # print(soup.text)

        except (ConnectionError, ConnectionResetError):
            pass

        apartment_list = []
        df = self.create_df()
        # print(f"made the dataframe: {df}")

        for floor_plan_table in soup.find_all(
            "table", {"data-testid": "floor-plan-group"}
        ):
            for tr in floor_plan_table.find_all("tr"):

                unit = tr.find("div", {"color": "highlight"}).text
                # print(unit)

                sqft = tr.find(
                    "td",
                    {"class": "FloorPlanTable__FloorPlanFloorSpaceCell-sc-1ghu3y7-5"},
                ).text

                bed = tr.find_all(
                    "td",
                    {"class": "FloorPlanTable__FloorPlanFeaturesCell-sc-1ghu3y7-4"},
                )[0].text

                bath = tr.find_all(
                    "td",
                    {"class": "FloorPlanTable__FloorPlanFeaturesCell-sc-1ghu3y7-4"},
                )[1].text

                price = tr.find_all(
                    "td",
                    {
                        "class": "FloorPlanTable__FloorPlanCell-sc-1ghu3y7-2",
                        "class": "FloorPlanTable__FloorPlanSMCell-sc-1ghu3y7-8",
                    },
                    limit=2,
                )[1].text

                name = soup.find(
                    "span", {"data-testid": "home-details-summary-headline"}
                ).text

                address = soup.find_all(
                    "span", {"data-testid": "home-details-summary-city-state"}
                )[0].text

                city_state_zip = soup.find_all(
                    "span", {"data-testid": "home-details-summary-city-state"}
                )[1].text

                city, state, zipcode = city_state_zip.replace(",", "").rsplit(
                    maxsplit=2
                )

                description = soup.find(
                    "div", {"data-testid": "home-description-text-description-text"}
                ).text

                details = [
                    detail.text
                    for detail in soup.find_all(
                        "li", {"class": "FeatureList__FeatureListItem-iipbki-0 dArMue"}
                    )
                ]
                details = " ,".join(details)

                apartment_url = base_url + current_url
                date = str(dt.now().date())

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [
                                {
                                    "name": name,
                                    "address": address,
                                    "unit": unit,
                                    "sqft": sqft,
                                    "bed": bed,
                                    "bath": bath,
                                    "price": price,
                                    "city": city,
                                    "state": state,
                                    "zipcode": zipcode,
                                    "description": description,
                                    "details": details,
                                    "url": apartment_url,
                                    "date": date,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )
        return df

    def get_all_apartments(self, base_url, url_list):
        """
        Wrapper function using "get_apartment_data" function to get data for all apartments in "url_list"
        """

        apts_data = self.create_df()
        for i, current_url in enumerate(
            tqdm(url_list.iloc[:, 1].to_list(), unit="sites"), start=1
        ):
            if i % 10 == 0:
                apts_data.to_csv("DATA/scrape_files/partial.csv")
            # print(current_url)
            time.sleep(3)
            apts_data = pd.concat(
                [apts_data, self.get_apartment_data(base_url, current_url)],
                ignore_index=True,
            )
            print(apts_data.tail(1))
        return apts_data

    def create_df(self):
        df = pd.DataFrame(
            columns=[
                "name",
                "address",
                "unit",
                "sqft",
                "bed",
                "bath",
                "price",
                "city",
                "state",
                "zipcode",
                "description",
                "details",
                "url",
                "date",
            ]
        )
        return df

    def df_converter(self, df):
        """Converts rows to numeric and float for calculations"""
        df = df.astype(
            {"sqft": "int32", "price": "int32", "bath": "float32", "bed": "float32"}
        )

        return df


def main():
    """ MAIN """


if __name__ == "__main__":
    main()

    print(f"Starting...")
    bot = SiteReader()
    # ulist = bot.get_url_list()
    # to_save = pd.DataFrame(ulist)
    # to_save.to_csv("current_listings.csv")
    url_list = pd.read_csv("listings.csv")

    test_url = url_list.iloc[2][1]
    base_url = "https://www.trulia.com"
    page_url = "/for_rent/Austin,TX/"

    # TODO: figure out how to handle housing rentals #1392

    # apts_data = bot.get_all_apartments(base_url, url_list)
    # print(f"Apartments retrieved: {len(apts_data)}")
    # to_save = pd.DataFrame(apts_data)
    # to_save.to_csv("current_apt_data.csv")
