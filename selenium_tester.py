# Data Basics
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

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
print(f"Chrome headless is set to: {chrome_options.headless}")
driver = webdriver.Chrome(options=chrome_options)



# driver = webdriver.Chrome()
# driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
# driver.get("http://www.google.com/")
# lucky_button = driver.find_element_by_css_selector("[name=btnI]") # So I picked something else --> .ktLKi
# lucky_button = driver.find_element_by_css_selector(".ktLKi")
# lucky_button.click()

# capture the screen
# driver.get_screenshot_as_file("capture.png")

# class SiteReader:
#     def __init__(self):
#         """ Headless options for script """
#         # chrome_options = Options()
#         # Comment out when developing / debugging
#         # chrome_options.add_argument("--no-sandbox")
#         # chrome_options.add_argument("--headless")
#         # chrome_options.add_argument("--window-size=800,600")
#         # chrome_options.add_argument("--remote-debugging-port=9222")
#         # print(f"Chrome headless is set to: {chrome_options.headless}")
#         # self.driver = webdriver.Chrome(options=chrome_options)

#         # Prototyping
#         # self.driver = webdriver.Chrome()

#         # self.driver.get("https://www.aol.com")
#         # self.driver.get()

#         # if webdriver gets stuck in headless mode, webdriver.ChromeOptions.set_headless=False

def main():
    """ MAIN """


if __name__ == "__main__":
    main()

    print(f"Starting...")
    os.system("echo $DISPLAY")
    # bot = SiteReader()

# xpath for "Please verify you are a human"
# /html/body/section/div[2]/h1