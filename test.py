import pandas as pd


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def scrape_site_questions():
    from selenium import webdriver
    import pandas as pd
    import time
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.by import By
    import re
    import math
    import openpyxl
    from geopy.geocoders import Nominatim
    from openpyxl.styles import Alignment
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(
        executable_path='chromedriver_win32/chromedriver.exe'
        , options=options)


    data = pd.read_excel('add_q.xlsx')
    ids = list(data['Id'])
    print(ids)

    # geoLocator = Nominatim(
    # user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
    # timeout=3)
    # for i in questions.keys():
    #     if i not in processed_ids:
    #         if (questions[i][11] != "No Location"):
    #             location = geoLocator.geocode(questions[i][11])
    #             if location is not None:
    #                 questions[i].append(location.latitude)
    #                 questions[i].append(location.longitude)
    #             else:
    #                 questions[i].append("None")
    #                 questions[i].append("None")
    #         else:
    #             questions[i].append("None")
    #             questions[i].append("None")

print('Extracting Question Data')
#

scrape_site_questions()
