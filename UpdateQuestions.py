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
question_id = []


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='chromedriver_win32/chromedriver.exe'
    , options=options)

for question in question_id:
    lista = []  # [votes,comments,answers,closed,views,first_date]
    url = "https://stackoverflow.com/questions/"+question['question_id'].split("-")[2]
    try:
        driver.get(url)
        question_text = driver.find_element_by_id('question')
        votes = driver.find_element_by_xpath('//div[contains(@class, "js-vote-count")]')
        lista.append(votes.text)
        try:
            comments_link = question_text.find_element_by_css_selector(".js-show-link.comments-link")
            driver.execute_script("arguments[0].click();", comments_link)
            time.sleep(3)
            comment_number = question_text.find_elements_by_class_name("comment-copy")
            lista.append(len(comment_number))
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            try:
                comment_number = question_text.find_elements_by_class_name("comment-copy")
                lista.append(len(comment_number))
            except (NoSuchElementException, IndexError, StaleElementReferenceException):
                lista.append('No comments')
        try:
            answers = driver.find_element_by_xpath("//div[contains(@id,'answers-header')]//*[contains(@class,'flex--item')]"
                                                "//*[contains(@class,'mb0')]")
            answers = answers.text
            answers_number = [int(s) for s in answers.split() if s.isdigit()]
            lista.append(answers_number[0])
        except (NoSuchElementException,IndexError,StaleElementReferenceException):
            lista.append(0)
        try:
            closed_date = driver.find_element_by_xpath('//*[contains(@class,"s-notice")]')
            if closed_date.is_displayed():
                lista.append(1)
            else:
                lista.append(0)
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            lista.append(0)
        time.sleep(2)
        views = driver.find_element_by_xpath('//*[contains(@title,"Viewed")]')
        lista.append(views.get_attribute('title'))
        print(lista)
        collection.update_one(
            {"question_id" : question },
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
            {"question_id": question},
            {"$set":
                {
                    "deleted": 1,
                }
            }
        )
