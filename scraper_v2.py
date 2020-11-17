# Data Basics
import pandas as pd
import numpy as np
from datetime import datetime as dt

pd.options.display.float_format = "{:.0f}".format

# scraping
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# to install ChromeDriverManager() on first use
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=400,300")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-dev-shm-usage")
# webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# webdriver.Chrome(ChromeDriverManager().install())


import time
import requests
from tqdm import tqdm
import os

import concurrent.futures


class SiteReader:
    def __init__(self):
        """ Headless options for script """
        chrome_options = Options()
        # Comment out when developing / debugging
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=400,300")
        chrome_options.add_argument("--remote-debugging-port=9222")
        print(f"Chrome headless is set to: {chrome_options.headless}")
        # self.driver = webdriver.Chrome(options=chrome_options)

        # Prototyping
        self.driver = webdriver.Chrome()

        # if webdriver gets stuck in headless mode, webdriver.ChromeOptions.set_headless=False
        base_url = "https://www.trulia.com"
        city_url = "/for_rent/Austin,TX/"

    def get_url_list(self, base_url, city_url):
        """Gets a list of urls from main page to scrape."""
        # self.driver.get(
        #     "https://www.trulia.com/for_rent/Austin,TX/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/"
        # )\

        url_list = []
        last_page = False
        i = 1

        # while last_page == False and i < 100:  # 100 picked because 92 pages for austin
        while last_page == False:
            time.sleep(3)
            self.driver.get(base_url + city_url)  # city + page of site
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
                city_url = soup.find("a", {"aria-label": "Next Page"})["href"]
                # print(city_url)
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

        # Is this an apartment complex with a table to parse?
        if soup.find_all("table", {"data-testid": "floor-plan-group"}) != []:
            for floor_plan_table in soup.find_all(
                "table", {"data-testid": "floor-plan-group"}
            ):
                for tr in floor_plan_table.find_all("tr"):

                    unit = tr.find("div", {"color": "highlight"}).text
                    # print(unit)

                    sqft = tr.find(
                        "td",
                        {
                            "class": lambda L: L
                            and L.startswith("FloorPlanTable__FloorPlanFloorSpaceCell")
                        },
                    ).text

                    bed = tr.find_all(
                        "td",
                        {
                            "class": lambda L: L
                            and L.startswith("FloorPlanTable__FloorPlanFeaturesCell")
                        },
                    )[0].text

                    bath = tr.find_all(
                        "td",
                        {
                            "class": lambda L: L
                            and L.startswith("FloorPlanTable__FloorPlanFeaturesCell")
                        },
                    )[1].text

                    price = tr.find_all(
                        "td",
                        {
                            "class": lambda L: L
                            and L.startswith("FloorPlanTable__FloorPlanCell"),
                            "class": lambda L: L
                            and L.startswith("FloorPlanTable__FloorPlanSMCell"),
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
                            "li",
                            {
                                "class": lambda L: L
                                and L.startswith("FeatureList__FeatureListItem")
                            },
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
            else:  # must be a home condo
                home_deets = soup.find_all(
                    "div", {"data-testid": "home-details-summary-container"}
                )
                price = (
                    home_deets[0]
                    .find_all("div", lambda L: L and L.startswith("Text__TextBase"))[0]
                    .text
                )
                bed = (
                    home_deets[0]
                    .find_all(
                        "div", lambda L: L and L.startswith("MediaBlock__MediaContent")
                    )[0]
                    .text
                )
                bath = (
                    home_deets[0]
                    .find_all(
                        "div", lambda L: L and L.startswith("MediaBlock__MediaContent")
                    )[1]
                    .text
                )
                sqft = (
                    home_deets[0]
                    .find_all(
                        "div", lambda L: L and L.startswith("MediaBlock__MediaContent")
                    )[2]
                    .text
                )
                name = (
                    home_deets[0]
                    .find_all("span", {"data-testid": "home-details-summary-headline"})[
                        0
                    ]
                    .text
                )
                address = (
                    home_deets[0]
                    .find_all("span", {"data-testid": "home-details-summary-headline"})[
                        0
                    ]
                    .text
                )
                city_state_zip = (
                    home_deets[0]
                    .find_all(
                        "span", {"data-testid": "home-details-summary-city-state"}
                    )[0]
                    .text
                )
                city, state, zipcode = city_state_zip.replace(",", "").rsplit(
                    maxsplit=2
                )
                description = soup.find_all(
                    "div", {"data-testid": "home-description-text-description-text"}
                )[0].text
                details = [
                    detail.text
                    for detail in soup.find_all(
                        "li",
                        {
                            "class": lambda L: L
                            and L.startswith("FeatureList__FeatureListItem")
                        },
                    )
                ]
                unit = "home"
                date = str(dt.now().date())
                apartment_url = base_url + current_url
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

    def get_all_apartments(self, base_url, url_list, city, state):
        """
        Wrapper function using "get_apartment_data" function to get data for all apartments in "url_list"
        """

        apts_data = self.create_df()
        for i, current_url in enumerate(
            tqdm(url_list.iloc[:, 1].to_list(), unit="site"), start=1
        ):
            if i % 10 == 0:
                apts_data.to_csv(f"DATA/scrape_files/partial_{city}_{state}.csv")
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


def main(i, city_state):
    """ MAIN """
    bot = SiteReader()
    base_url = "https://www.trulia.com"
    today = int(dt.today().strftime("%Y%m%d"))
    city, state = city_state

    city_url = f"/for_rent/{city},{state}/"
    residence_urls = f"DATA/urls/apt_page_listings_{city}_{state}_{today}.csv"
    unit_info = f"DATA/scrape_files/apt_unit_listings_{city}_{state}_{today}.csv"

    # Generate list of URLs to walk through, skip if saved list is recent
    for i in range(7):
        if os.path.isfile(
            f"DATA/urls/apt_page_listings_{city}_{state}_{today - i}.csv"
        ):
            url_list = pd.read_csv(
                f"DATA/urls/apt_page_listings_{city}_{state}_{today - i}.csv"
            )
            break  # only breaks one-level out of for-loop
        elif i < 6:
            continue
        else:
            print("No recent file found, generating new list")
            ulist = bot.get_url_list(base_url, city_url)
            to_save = pd.DataFrame(ulist)
            to_save.to_csv(residence_urls)
            url_list = pd.read_csv(residence_urls)

    # Find all the units available for a listing
    if os.path.isfile(unit_info):
        print("units file found")
    else:
        print("units file not found")
        apts_data = bot.get_all_apartments(base_url, url_list, city, state)
        to_save = pd.DataFrame(apts_data)
        to_save.to_csv(unit_info)


if __name__ == "__main__":
    print(f"Starting...")
    os.system(
        "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0"
    )
    os.system("echo $DISPLAY")

    cities = [
        ["Chicago", "IL"],
        ["Saint_Louis", "MO"],
        ["New_York", "NY"],
        ["Las_Vegas", "NV"],
        ["Dallas", "TX"],
        ["Portland", "OR"],
        ["Seattle", "WA"],
        ["Minneapolis", "MN"],
        ["Orlando", "FL"],
        ["San_Francisco", "CA"],
        ["Austin", "TX"],
        ["Ann_Arbor", "MI"],
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, city_state in enumerate(tqdm(cities, unit="city"), start=1):
            executor.map(main, [i, city_state])