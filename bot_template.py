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

### don't load images ###
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
print(f"Chrome Options are set to: {chrome_options.arguments}")


# Easy way to launch Xvfb display in Python
# from pyvirtualdisplay import Display

# disp = Display(visible=False)
# disp.start()


if __name__ == "__main__":
    bot.driver = webdriver.Chrome(options=chrome_options)