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

# Chrome WebDriver stuff
chrome_options = Options()
### Use Headless ###
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
# print(f"Chrome headless is set to: {chrome_options.headless}")

chrome_options.add_argument("--window-size=800,800")

### don't load images ###
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# print(f"Chrome Options are set to: {chrome_options.arguments}")


# Easy way to launch Xvfb display in Python
# from pyvirtualdisplay import Display

# disp = Display(visible=False)
# disp.start()


if __name__ == "__main__":
    url = "https://www.trulia.com/c/tx/austin/regency-601-w-11th-st-austin-tx-78701--2110329431"
    bot = webdriver.Chrome(options=chrome_options)
    response = bot.get(url)
    html = bot.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(html, "lxml")

    # debugging for missing 'details' in output
    for floor_plan_table in soup.find_all("table", {"data-testid": "floor-plan-group"}):
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

            city, state, zipcode = city_state_zip.replace(",", "").rsplit(maxsplit=2)

            description = soup.find(
                "div", {"data-testid": "home-description-text-description-text"}
            ).text

            details = [
                detail.text
                for detail in soup.find_all(
                    "li",
                    {"class": lambda L: L and L.startswith("Feature__FeatureListItem")},
                )
            ]
            details = " ,".join(details)
