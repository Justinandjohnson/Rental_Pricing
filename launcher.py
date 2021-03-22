import os
import re
import concurrent.futures

from Scrapers import Trulia

### Run Singular Test ###
# bot = Trulia(["Ann_Arbor", "MI"])


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
    bot = executor.map(Trulia, cities)

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     # make these a list comprehension
#     bot01 = executor.submit(Trulia, "Austin", "TX")
#     bot02 = executor.submit(Trulia, "Dallas", "TX")
#     bot03 = executor.submit(Trulia, "Saint_Louis", "MO")
#     bot04 = executor.submit(Trulia, "New_York", "NY")
#     bot05 = executor.submit(Trulia, "Chicago", "IL")
#     bot06 = executor.submit(Trulia, "Las_Vegas", "NV")
#     bot07 = executor.submit(Trulia, "Portland", "OR")
#     bot08 = executor.submit(Trulia, "Seattle", "WA")
#     bot09 = executor.submit(Trulia, "Minneapolis", "MN")
#     bot10 = executor.submit(Trulia, "Orlando", "FL")
#     bot11 = executor.submit(Trulia, "San_Francisco", "CA")
#     bot12 = executor.submit(Trulia, "Ann_Arbor", "MI")


