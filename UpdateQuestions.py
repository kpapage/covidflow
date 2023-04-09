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
from selenium.webdriver.common.by import By

print('Extracting Question Data')
cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='chromedriver_win32/chromedriver.exe'
    , options=options)

for question in collection.find(no_cursor_timeout=True).batch_size(30):
    lista = []  # [votes,comments,answers,closed,views,first_date]
    url = "https://stackoverflow.com/questions/"+question['question_id'].split("-")[2]
    try:
        driver.get(url)
        question_text = driver.find_element(By.ID,'question')
        votes = driver.find_element(By.XPATH,'//div[contains(@class, "js-vote-count")]')
        lista.append(votes.text)
        try:
            answers = driver.find_elements(By.XPATH,
                                           "//div[contains(@id, 'answers')]//div[contains(@class, 'answercell')]")
            print(len(answers))
            time.sleep(5)
            timestamps = []
            for answer in answers:
                timestamp_list = answer.find_elements(By.XPATH,"//div[contains(@class, 'answercell')]//span[contains(@class, 'relativetime')]")
                for element in timestamp_list:
                    timestamps.append(element.get_attribute('title'))
            print(timestamps)
            if not timestamps:
                collection.update_one(
                    {"question_id": question['question_id']},
                    {"$set":
                        {
                            "first_answer": 'No answers'
                        }
                    }
                )
            else:
                if len(timestamps) == 1:
                    collection.update_one(
                        {"question_id": question['question_id']},
                        {"$set":
                            {
                                "first_answer": timestamps[0]
                            }
                        }
                    )
                else:
                    first_answer = min(timestamps)
                    print(first_answer)
                    collection.update_one(
                        {"question_id": question['question_id']},
                        {"$set":
                            {
                                "first_answer": first_answer
                            }
                        }
                    )
        except NoSuchElementException:
             pass
        try:
            comments_link = question_text.find_element(By.CSS_SELECTOR,".js-show-link.comments-link")
            driver.execute_script("arguments[0].click();", comments_link)
            time.sleep(3)
            comment_number = question_text.find_elements(By.CLASS_NAME,"comment-copy")
            lista.append(len(comment_number))
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            try:
                comment_number = question_text.find_elements(By.CLASS_NAME,"comment-copy")
                lista.append(len(comment_number))
            except (NoSuchElementException, IndexError, StaleElementReferenceException):
                lista.append('No comments')
        try:
            answers = driver.find_element(By.XPATH,"//div[contains(@id,'answers-header')]//*[contains(@class,'flex--item')]"
                                                "//*[contains(@class,'mb0')]")
            answers = answers.text
            answers_number = [int(s) for s in answers.split() if s.isdigit()]
            lista.append(answers_number[0])
        except (NoSuchElementException,IndexError,StaleElementReferenceException):
            lista.append(0)
        try:
            closed_date = driver.find_element(By.XPATH,'//*[contains(@class,"s-notice")]')
            if closed_date.is_displayed():
                lista.append(1)
            else:
                lista.append(0)
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            lista.append(0)
        time.sleep(2)
        views = driver.find_element(By.XPATH,'//*[contains(@title,"Viewed")]')
        lista.append(views.get_attribute('title'))
        print(lista)
        collection.update_one(
            {"question_id" : question['question_id'] },
            {"$set":
                {
                    "votes" : lista[0],
                    "comments" : lista[1],
                    "answers" : lista[2],
                    "closed" : lista[3],
                    "views" : lista[4],
                }
            }
        )
    except NoSuchElementException:
        collection.update_one(
            {"question_id": question['question_id']},
            {"$set":
                {
                    "deleted": 1,
                }
            }
        )