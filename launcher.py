import os
import re
import concurrent.futures

from Scrapers import Trulia

### Run Singular Test ###
# bot = Trulia(["Ann_Arbor", "MI"])


cities = [
    ["New_York", "NY"],
    ["Los_Angeles", "CA"],
    ["Chicago", "IL"],
    ["Houston", "TX"],
    ["Philadelphia", "PA"],
    ["Phoenix", "AZ"],
    ["San_Antonio", "TX"],
    ["San_Diego", "CA"],
    ["Dallas", "TX"],
    ["San_Jose", "CA"],
    ["Austin", "TX"],
    ["Jacksonville", "FL"],
    ["San_Francisco", "CA"],
    ["INpolis", "In"],
    ["Columbus", "Oh"],
    ["Fort_Worth", "Tx"],
    ["Charlotte", "NC"],
    ["Detroit", "MI"],
    ["El_Paso", "TX"],
    ["Seattle", "WA"],
    ["Denver", "CO"],
    ["Washington", "DC"],
    ["Memphis", "TN"],
    ["Boston", "MA"],
    ["Nashville", "TN"],
    ["Baltimore", "MD"],
    ["Oklahoma_City", "OK"],
    ["Portland", "OR"],
    ["Las_Vegas", "NV"],
    ["Louisville", "KY"],
    ["Milwaukee", "WI"],
    ["Albuquerque", "NM"],
    ["Tucson", "AZ"],
    ["Fresno", "CA"],
    ["Sacramento", "CA"],
    ["Long_Beach", "CA"],
    ["KS_City", "MO"],
    ["Mesa", "AZ"],
    ["Atlanta", "Georgia"],
    ["VA_Beach", "VA"],
    ["Omaha", "NE"],
    ["Colorado_Springs", "CO"],
    ["Raleigh", "NC"],
    ["Miami", "FL"],
    ["Oakland", "CA"],
    ["Minneapolis", "MN"],
    ["Tulsa", "OK"],
    ["Cleveland", "OH"],
    ["Wichita", "KS"],
    ["New", "Orleans", "LA"],
    ["Arlington", "TX"],
    ["Bakersfield", "CA"],
    ["Tampa", "FL"],
    ["Aurora", "CO"],
    ["Honolulu", "HI"],
    ["Anaheim", "CA"],
    ["Santa", "Ana", "CA"],
    ["Corpus", "Christi", "TX"],
    ["Riverside", "CA"],
    ["Saint_Louis", "MO"],
    ["Lexington", "KY"],
    ["Pittsburgh", "PA"],
    ["Stockton", "CA"],
    ["Anchorage", "AK"],
    ["Cincinnati", "OH"],
    ["Saint_Paul", "MN"],
    ["Greensboro", "NC"],
    ["Toledo", "OH"],
    ["Newark", "NJ"],
    ["Plano", "TX"],
    ["Henderson", "NV"],
    ["Lincoln", "NE"],
    ["Orlando", "FL"],
    ["Jersey_City", "NJ"],
    ["Chula_Vista", "CA"],
    ["Buffalo", "NY"],
    ["Fort_Wayne", "IN"],
    ["Chandler", "AZ"],
    ["Saint_Petersburg", "FL"],
    ["Laredo", "TX"],
    ["Durham", "NC"],
    ["Irvine", "CA"],
    ["Madison", "WI"],
    ["Norfolk", "VA"],
    ["Lubbock", "TX"],
    ["Gilbert", "AZ"],
    ["Winston-Salem", "NC"],
    ["Glendale", "AZ"],
    ["Reno", "NV"],
    ["Hialeah", "FL"],
    ["Garland", "TX"],
    ["Chesapeake", "VA"],
    ["Irving", "TX"],
    ["North_Las_Vegas", "NV"],
    ["Scottsdale", "AZ"],
    ["Baton_Rouge", "LA"],
    ["Fremont", "CA"],
    ["Richmond", "VA"],
    ["Boise", "Id"],
    ["San_Bernardino", "CA"],
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
