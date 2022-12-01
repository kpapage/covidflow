import pymongo
from datetime import date
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re
import math
import openpyxl
from geopy.geocoders import Nominatim
from datetime import datetime

print('Extracting Question Data')
cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]
questions = collection.find()


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='chromedriver_win32/chromedriver.exe'
    , options=options)

for question in questions:
    if question['first_answer'] == 'No answers' or question['first_answer'] == 'Not':
        url = "https://stackoverflow.com/questions/" + question['question_id'].split("-")[2]
        try:
            driver.get(url)
            question_text = driver.find_element_by_id('question')
            try:
                answers = driver.find_elements_by_xpath("//div[contains(@class, 'answercell')]")
                time.sleep(2)
                timestamps = []
                for answer in answers:
                    timestamp = answer.find_element_by_xpath("//span[contains(@class, 'relativetime')]")
                    timestamps.append(timestamp.get_attribute('title'))
                print(timestamps)
                if not timestamps:
                    collection.update_one(
                        {"question_id": question},
                        {"$set":
                            {
                                "first_answer": 'No answers'
                            }
                        }
                    )
                else:
                    if len(timestamps) == 1:
                        collection.update_one(
                            {"question_id": question},
                            {"$set":
                                {
                                    "first_answer": timestamps[0]
                                }
                            }
                        )
                    else:
                        max = -10
                        for timestamp in timestamps:
                            d = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%SZ")
                            sum = d.year + d.month + d.day + d.hour + d.minute + d.second
                            if sum > max:
                                first_answer = timestamp
                        collection.update_one(
                            {"question_id": question},
                            {"$set":
                                {
                                    "first_answer": first_answer
                                }
                            }
                        )
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            collection.update_one(
                {"question_id": question},
                {"$set":
                    {
                        "first_answer": 'No answers'
                    }
                }
            )
