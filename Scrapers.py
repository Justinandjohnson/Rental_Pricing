import pandas as pd
import numpy as np
from datetime import datetime as dt
import time, requests, os, re
from tqdm import tqdm

# scraping stuff
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

# Easy way to launch Xvfb display in Python
from pyvirtualdisplay import Display

disp = Display(visible=False)
disp.start()

# Set logging level (current output to consol only)
import logging

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s:%(funcName)s:%(process)d:%(message)s"
)

### Changes ###
# pass city, state - DONE
# @staticmethod cleanup - DONE
# Tweak URL scraping to include last page - DONE
# FIX details section of output :'(
# add house rentals and other offerings
# add Zillow


class Trulia:
    def __init__(self, city_state):
        """ Construct the object and launch a browser window """
        # Set options for chrome
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # Start a bowser
        self.driver = webdriver.Chrome(options=chrome_options)

        # randomly delay start, for multiprocessing
        self.startup_delay = int(np.random.rand() * 60)
        logging.warning(f"Stating Chrome... in {self.startup_delay} seconds")
        time.sleep(self.startup_delay)

        # Set attributes
        self.base_url = "https://www.trulia.com"
        self.city = city_state[0]
        self.state = city_state[1]
        self.city_url = f"/for_rent/{self.city},{self.state}/"
        self.delay = 10
        self.reCaptcha_delay = 300
        self.today = int(dt.today().strftime("%Y%m%d"))
        self.url_expiration = 20  # set random days a url file is valid b/w 5-20

        # Set Data Save Locations:
        self.residence_urls = (
            f"DATA/urls/apt_page_listings_{self.city}_{self.state}_{self.today}.csv"
        )

        self.unit_info = f"DATA/scrape_files/apt_unit_listings_{self.city}_{self.state}_{self.today}.csv"
        self.partial = (
            f"DATA/scrape_files/partial_{self.city}_{self.state}_{self.today}.csv"
        )
        self.page = 1
        self.url_list = []
        self.recaptcha_url_counter = 0
        self.recaptcha_apt_counter = 0

    def get_url_list(self):
        """Gets a list of URLs for each appartment in the city of interest.
        Works through each page in a city until it finds the last page."""

        # Initialize some variables
        self.last_page = False
        self.page = 1

        while self.last_page == False:
            time.sleep(self.delay)
            logging.debug(self.base_url + self.city_url)

            # Open next page and get the soup
            self.driver.get(self.base_url + self.city_url)
            soup = BeautifulSoup(
                self.driver.execute_script("return document.body.innerHTML;"),
                features="lxml",
            )

            # check if on last page and exit loop if True
            if soup.find("a", {"aria-label": "Next Page"}):
                # Find all urls on page and append to list - Nested due to reCaptcha
                urls = self.locate_urls(soup)
                self.url_list.extend(urls)

                # Move to the next page and increment counter
                self.city_url = soup.find("a", {"aria-label": "Next Page"})["href"]
                self.page += 1

            # Test for reCaptcha
            elif soup.find("h1").text == "Please verify you are a human":
                logging.warning("URL INFO - RECAPTCHA!!!!")
                # do something with reCAPTCHA
                self.recaptcha_url_counter += 1
                if self.recaptcha_url_counter > 10:
                    self.toggle_vpn()
                time.sleep(self.reCaptcha_delay)
                pass
            else:
                urls = self.locate_urls(soup)
                self.url_list.extend(urls)
                self.last_page = True

            logging.info(
                f"Finished Page: {self.page} which has a last listing of: {self.url_list[-1]}"
            )
        return self.url_list

    def get_all_apartments(self):
        """
        Wrapper function using "get_apartment_data" function to get data for all apartments in "url_list"
        """
        # Set URL list by checking if the list has been generated lately
        self.url_list = self.are_urls_current()
        logging.debug(self.url_list)
        apts_data = self.create_df()
        for i, current_url in enumerate(
            tqdm(self.url_list.iloc[:, 1].to_list(), unit="site", desc=self.city),
            start=1,
        ):
            # Save partial data every 10 sites
            if i % 10 == 0:
                apts_data.to_csv(self.partial)
            logging.debug(f"The Current URL is: {current_url}")
            time.sleep(self.delay)
            apts_data = pd.concat(
                [apts_data, self.get_apartment_data(current_url)],
                ignore_index=True,
            )
            logging.debug(apts_data.tail(1))
        apts_data.to_csv(self.unit_info)

    def get_apartment_data(self, current_url):
        """Gets apartment data for the url specified"""
        time.sleep(self.delay)
        try:
            logging.debug(self.base_url + current_url)
            response = self.driver.get(self.base_url + current_url)
            html = self.driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(html, "lxml")
            apartment_url = self.base_url + current_url
            df = self.create_df()
            logging.debug(soup.text)

        except (ConnectionError, ConnectionResetError):
            pass

        # Test for reCaptcha
        if soup.find("h1").text == "Please verify you are a human":
            logging.warning("APT INFO - RECAPTCHA!!!!")
            # deal with recaptcha
            self.recaptcha_apt_counter += 1
            if self.recaptcha_apt_counter > 10:
                self.toggle_vpn()
            time.sleep(self.reCaptcha_delay)

        # Is this an apartment complex with a table to parse?
        if soup.find_all("table", {"data-testid": "floor-plan-group"}) != None:
            return self.locate_apt_table_info(soup, df, apartment_url)

        # else return condo info
        return self.locate_condo_info(soup, df)

    def are_urls_current(self):
        """ Checks if the current list of URLs is current for the city """

        # Load recent file if it exists
        for i in range(self.url_expiration):
            url_csv = f"DATA/urls/apt_page_listings_{self.city}_{self.state}_{self.today - i}.csv"
            if os.path.isfile(url_csv):
                logging.debug(f"Found file {url_csv} \nLoading it now...")
                self.url_list = pd.read_csv(url_csv)
                return self.url_list

        # Generate list, save to file, and return list
        logging.debug("No recent file found, generating new list of URLs")
        to_save = pd.DataFrame(self.get_url_list())
        to_save.to_csv(self.residence_urls)
        self.url_list = pd.read_csv(self.residence_urls)
        return self.url_list

    def are_apts_current(self):
        """ Check if aptartments have been scanned today """

        if os.path.isfile(self.unit_info):
            logging.debug("Appartment units file found")
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

    @staticmethod
    def locate_urls(soup):
        """ BeautifulSoup Filter to find all URLs (to scrape) on the page """
        urls = []
        if soup is not None:

            for div in soup.find_all(
                "div",
                {
                    "data-hero-element-id": "srp-home-card",
                    "data-hero-element-id": "false",
                },
            ):
                url = div.find("a").attrs["href"]
                urls.append(url)

        return urls

    @staticmethod
    def locate_apt_table_info(soup, df, apartment_url):
        """ Parse appartment listing table and return DataFrame """

        for floor_plan_table in soup.find_all(
            "table", {"data-testid": "floor-plan-group"}
        ):
            for tr in floor_plan_table.find_all("tr"):

                unit = tr.find("div", {"color": "highlight"}).text
                # logging.debug(unit)

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

    @staticmethod
    def locate_condo_info(soup, df):
        """ locates information for House, Condos, and anything else for rent that isn't an appartment """

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
                .find_all("span", {"data-testid": "home-details-summary-headline"})[0]
                .text
            )
            address = (
                home_deets[0]
                .find_all("span", {"data-testid": "home-details-summary-headline"})[0]
                .text
            )
            city_state_zip = (
                home_deets[0]
                .find_all("span", {"data-testid": "home-details-summary-city-state"})[0]
                .text
            )
            city, state, zipcode = city_state_zip.replace(",", "").rsplit(maxsplit=2)
            description = soup.find_all(
                "div", {"data-testid": "home-description-text-description-text"}
            )[0].text
            details = [
                detail.text
                for detail in soup.find_all(
                    "li",
                    {"class": lambda L: L and L.startswith("Feature__FeatureListItem")},
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

    def toggle_vpn(self):
        """ Toggle VPN, in my case I use Windscribe """
        os.system("windscribe disconnect")
        time.sleep(10)
        os.system("windscribe connect best")
        self.recaptcha_url_counter = 0
        self.recaptcha_apt_counter = 0

    def __del__(self):
        self.driver.close()
        os.system(f"rm {self.partial}")
        logging.warning(
            f"Destructor called, webpage and partial file deleted after {self.city}, {self.state}"
        )
