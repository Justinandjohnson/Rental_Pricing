import pandas as pd
import numpy as np
from datetime import datetime as dt

pd.options.display.float_format = "{:.0f}".format

import time
import requests
from tqdm import tqdm
import os
import re

# scraping 'STUFF'
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

from pyvirtualdisplay import Display

disp = Display(visible=False)
disp.start()

chrome_options = Options()
### Use Headless ###
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
# print(f"Chrome headless is set to: {chrome_options.headless}")

# ua = UserAgent()
# userAgent = ua.random
# chrome_options.add_argument(f"user-agent={userAgent}")

### don't load images ###
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
print(f"Chrome Options are set to: {chrome_options.arguments}")


### Changes ###
# pass city, state
# @staticmethod cleanup
# add house rentals and other offerings
# add Zillow


class Trulia:
    def __init__(self, city, state):
        """ Headless options for script """
        # Question if nessessary to load here or in MAIN...?
        self.driver = webdriver.Chrome(options=chrome_options)

        # randomly delay start, for multiprocessing
        self.startup_delay = int(np.random.rand() * 60)
        print(f"Stating Chrome... in {self.startup_delay}")
        time.sleep(self.startup_delay)
        # self.driver.implicitly_wait(self.startup_delay)

        # Set attributes
        self.base_url = "https://www.trulia.com"
        self.city = city
        self.state = state
        self.city_url = f"/for_rent/{self.city},{self.state}/"
        self.delay = 10
        self.reCaptcha_delay = 300

        self.today = int(dt.today().strftime("%Y%m%d"))
        self.url_expiration = 15  # days a url file is valid
        self.residence_urls = (
            f"DATA/urls/apt_page_listings_{self.city}_{self.state}_{self.today}.csv"
        )

        self.unit_info = f"DATA/scrape_files/apt_unit_listings_{self.city}_{self.state}_{self.today}.csv"
        self.partial = (
            f"DATA/scrape_files/partial_{self.city}_{self.state}_{self.today}.csv"
        )
        self.page = 1

        # This kicks off the scraper
        self.are_apts_current()

    def get_url_list(self):
        """Gets a list of urls for each appartment in the city of interest.
        Works through each page on the list until it finds the last page."""

        self.url_list = []
        self.last_page = False
        self.page = 1

        while self.last_page == False:
            time.sleep(self.delay)
            print(self.base_url + self.city_url)

            # Open next page and get the soup
            self.driver.get(self.base_url + self.city_url)
            soup = BeautifulSoup(
                self.driver.execute_script("return document.body.innerHTML;"),
                features="lxml",
            )

            # TODO, need to tweak this, currently doesn not scan the last page
            # check if last page and exit while loop if True
            if soup.find("a", {"aria-label": "Next Page"}):
                # Find all urls on page and append to list
                for div in soup.find_all(
                    "div",
                    {
                        "data-hero-element-id": "srp-home-card",
                        "data-hero-element-id": "false",
                    },
                ):
                    # print(div)
                    url = div.find("a").attrs["href"]
                    self.url_list.append(url)

                self.last_page = False
                self.city_url = soup.find("a", {"aria-label": "Next Page"})["href"]
                time.sleep(self.delay)
            # Test for reCaptcha
            elif soup.find("h1").text == "Please verify you are a human":
                print("URL INFO - RECAPTCHA!!!!")
                # turn headless off and open
                time.sleep(self.reCaptcha_delay)
                pass
            else:
                self.last_page = True

            print(f"Page: {self.page} last listing: {self.url_list[-1]}")
            self.page += 1
        return self.url_list

    def get_all_apartments(self):
        """
        Wrapper function using "get_apartment_data" function to get data for all apartments in "url_list"
        """
        # Set URL list by checking if the list has been generated lately
        self.url_list = self.are_urls_current()
        print(self.url_list)
        apts_data = self.create_df()
        for i, current_url in enumerate(
            tqdm(self.url_list.iloc[:, 1].to_list(), unit="site"), start=1
        ):
            if self.page % 10 == 0:
                apts_data.to_csv(self.partial)
            print(f"The Current URL is: {current_url}")
            time.sleep(self.delay)
            apts_data = pd.concat(
                [apts_data, self.get_apartment_data(current_url)],
                ignore_index=True,
            )
            print(apts_data.tail(1))
        return apts_data

    def get_apartment_data(self, current_url):
        """Gets apartment data for the url specified"""
        try:
            time.sleep(self.delay)
            # print(self.base_url + current_url)
            response = self.driver.get(self.base_url + current_url)
            html = self.driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(html, "lxml")
            # print(soup.text)

        except (ConnectionError, ConnectionResetError):
            pass

        # Test for reCaptcha
        if soup.find("h1").text == "Please verify you are a human":
            print("APT INFO - RECAPTCHA!!!!")
            # deal with recaptcha
            time.sleep(self.reCaptcha_delay)

        self.apartment_list = []
        df = self.create_df()

        # Is this an apartment complex with a table to parse?
        if soup.find_all("table", {"data-testid": "floor-plan-group"}) != None:
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

                    apartment_url = self.base_url + current_url
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
        else:  # a home, condo, etc... not an apt complex
            try:
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
            except Exception as e:
                pass
        return df

    def are_urls_current(self):
        """ Checks if the current list of URLs is current for the city """

        for i in range(self.url_expiration):
            url_csv = f"DATA/urls/apt_page_listings_{self.city}_{self.state}_{self.today - i}.csv"
            if os.path.isfile(url_csv):
                print(f"Found file {url_csv} \nLoading it now...")
                url_list = pd.read_csv(url_csv)
                return url_list
                # break  # only breaks one-level out of for-loop

        print("No recent file found, generating new list of URLs")
        to_save = pd.DataFrame(self.get_url_list())
        to_save.to_csv(self.residence_urls)
        url_list = pd.read_csv(self.residence_urls)
        return url_list

    def are_apts_current(self):
        """ Check if aptartments have been scanned """

        if os.path.isfile(self.unit_info):
            print("units file found")
            return pd.read_csv(self.unit_info)

        self.unit_info = pd.DataFrame(self.get_all_apartments())
        self.unit_info.to_csv(self.unit_info)
        return pd.read_csv(self.unit_info)

    @staticmethod
    def create_df():
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

    @staticmethod
    def df_converter(df):
        """Converts rows to numeric and float for calculations"""
        df = df.astype(
            {"sqft": "int32", "price": "int32", "bath": "float32", "bed": "float32"}
        )

        return df