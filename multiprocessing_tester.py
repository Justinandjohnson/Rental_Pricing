from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import numpy as np


# Python program to illustrate destructor
class Trulia:
    # Initializing
    def __init__(self, city_state, auto_start=True):
        self.driver = webdriver.Chrome()

        self.delay = int(np.random.rand() * 10)
        print(f"Delay is {self.delay}")
        self.city_state = city_state
        print(f"Webpage created for {self.city_state}")
        time.sleep(self.delay)
        self.auto_start = auto_start
        if auto_start == True:
            self.something()

    def something(self):
        print(f"Doing something for {self.delay} for {self.city_state}")
        time.sleep(self.delay)

    # Deleting (Calling destructor)
    def __del__(self):
        self.driver.close()
        print(f"Destructor called, webpage deleted after {self.city_state}")


if __name__ == "__main__":
    bot = Trulia(["A", "B"])
