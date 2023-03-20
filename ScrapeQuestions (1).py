def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

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
from datetime import datetime
from openpyxl.styles import Alignment
import pymongo
import pickle
import ast
import itertools
from webdriver_auto_update import check_driver
import requests
import wget
import zipfile
import os
url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
response = requests.get(url)
version_number = response.text

# build the donwload url
download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

# download the zip file using the url built above
latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

# extract the zip file
with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
    zip_ref.extractall()  # you can specify the destination folder path here
# delete the zip file downloaded above
os.remove(latest_driver_zip)
with (open("xgb_model.pkl", "rb")) as openfile:
    while True:
        try:
            pickle.load(openfile)
        except EOFError:
            break
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='chromedriver.exe'
    , options=options)


print('Extracting Question Data')

tags = ["coronavirus", "corona-virus", "2019-ncov", "sars-cov",]

searchdate = "2022-11-1..2023-03-17"

list_of_dataframes = []
for tag in tags:
    print("Extracting question data about {}".format(tag))
    driver.get("https://stackoverflow.com/search?page=1&tab=Relevance&q={}%20created%3a{}%20{}%3a{}".format(tag, searchdate,'is','question'))
    results_text = driver.find_element(By.CSS_SELECTOR, ".flex--item.fl1.fs-body3.mr12").text
    numberOfResults = float(re.sub("[^0-9]", "", results_text))
    pages = math.ceil(numberOfResults / 15)
    questions = {}
    covered_ids = []
    processed_ids = []
    for i in range(pages):
        driver.get("https://stackoverflow.com/search?page={}&tab=Relevance&q={}%20created%3a{}%20{}%3a{}".format(i+1, tag, searchdate,'is','question'))
        try:
            lists = driver.find_elements(By.XPATH, '//*[contains(@id, "question-summary")]')
            for listitem in lists:
                metadata = []
                id = listitem.get_attribute('id')
                tags = listitem.find_elements(By.CSS_SELECTOR, '.js-post-tag-list-item')
                tag_list = []
                for tagg in tags:
                    tag_list.append(tagg.text)
                if type(tag_list) is list:
                    metadata.append(tag_list)
                else:
                    new_tag_list = []
                    for tag in tag_list.split(' '):
                        new_tag_list.append(tag)
                    metadata.append(new_tag_list)
                timestamp = listitem.find_element(By.CSS_SELECTOR, '.relativetime')
                metadata.append(timestamp.get_attribute('title'))
                items = listitem.find_elements(By.CSS_SELECTOR, '.s-post-summary--stats-item-number')
                item_list = []
                for item in items:
                    item_list.append(item.text)
                metadata.append(str(item_list[0]))
                metadata.append(item_list[1])
                try:
                    owner_id = listitem.find_element(By.CSS_SELECTOR, '.s-user-card--link.d-flex.gs4')
                    owner = owner_id.find_element(By.CSS_SELECTOR, '.flex--item')
                    metadata.append(owner.get_attribute('href'))
                except (NoSuchElementException, IndexError):
                    metadata.append('No Owner ID')
                time.sleep(3)
                questions[id] = metadata
        except NoSuchElementException:
            print('No questions in this page!')
    for id in questions.keys():
        if id not in covered_ids:
            split = id.split('-')
            idd = split[2]
            driver.get('https://stackoverflow.com/questions/{}'.format(idd))
            time.sleep(3)
            try:
                header = driver.find_element(By.ID, 'question-header')
                title = header.find_element(By.CLASS_NAME, 'question-hyperlink').text
                questions[id].append(title)
            except NoSuchElementException:
                print('Question not found/deleted')
                questions = removekey(questions, id)
                continue
            question_text = driver.find_element(By.ID, 'question')
            views = driver.find_element(By.XPATH, '//*[contains(@title,"Viewed")]')
            questions[id].append(views.get_attribute('title'))
            try:
                answers = driver.find_elements(By.XPATH,
                                               "//div[contains(@id, 'answers')]//div[contains(@class, 'answercell')]")
                timestamps = []
                for answer in answers:
                    timestamp = answer.find_element(By.XPATH,
                                                    "//div[contains(@class, 'answercell')]//span[contains(@class, 'relativetime')]")
                    timestamps.append(timestamp.get_attribute('title'))
                if not timestamps:
                    questions[id].append('No answers')
                if len(timestamps) == 1:
                    questions[id].append(timestamps[0])
                if len(timestamps) > 1:
                    max = -10
                    for timestamp in timestamps:
                        d = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%SZ")
                        sum = d.year + d.month + d.day + d.hour + d.minute + d.second
                        if sum > max:
                            first_answer = timestamp
                    questions[id].append(first_answer)
            except NoSuchElementException:
                questions[id].append('No answers')
            try:
                code_snippet = question_text.find_element(By.TAG_NAME, 'code')
                questions[id].append(1)
            except (NoSuchElementException, IndexError, StaleElementReferenceException):
                questions[id].append(0)
            try:
                comments_link = question_text.find_element(By.CSS_SELECTOR, ".js-show-link.comments-link")
                driver.execute_script("arguments[0].click();", comments_link)
                time.sleep(3)
                comment_number = question_text.find_elements(By.CLASS_NAME, "comment-copy")
                questions[id].append(len(comment_number))
            except (NoSuchElementException, IndexError, StaleElementReferenceException):
                try:
                    comment_number = question_text.find_elements(By.CLASS_NAME, "comment-copy")
                    questions[id].append(len(comment_number))
                except (NoSuchElementException, IndexError, StaleElementReferenceException):
                    questions[id].append('No comments')
            try:
                closed_date = driver.find_element(By.XPATH, '//*[contains(@class,"s-notice")]')
                if closed_date.is_displayed():
                    questions[id].append(1)
                else:
                    questions[id].append(0)
            except (NoSuchElementException, IndexError, StaleElementReferenceException):
                questions[id].append(0)
            post = question_text.find_element(By.CLASS_NAME, 'js-post-body')
            body = []
            bodies = post.find_elements(By.XPATH, '//*[contains(@class,"js-post-body")]//descendant::p')
            for bodyitem in bodies:
                body.append(bodyitem.text)
            body_joined = '.'.join(body)
            questions[id].append(body_joined)
            try:
                user_div = question_text.find_element(By.CSS_SELECTOR, '.post-signature.owner.flex--item')
                user_div2 = user_div.find_element(By.CLASS_NAME, 'user-details')
                user_link = user_div2.find_element(By.TAG_NAME, 'a')
                driver.execute_script("arguments[0].click();", user_link)
                time.sleep(3)
                try:
                    user_location = driver.find_element(By.CSS_SELECTOR, '.wmx2.truncate')
                    questions[id].append(user_location.text)
                except NoSuchElementException:
                    questions[id].append('No location')
            except NoSuchElementException:
                questions[id].append('No location')
            covered_ids.append(id)
            questions[id].append(0)  # for deleted
        else:
            questions = removekey(questions, id)
    geoLocator = Nominatim(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        timeout=3)
    for i in questions.keys():
        if i not in processed_ids:
            if (questions[i][12] != "No Location"):
                location = geoLocator.geocode(questions[i][12])
                if location is not None:
                    questions[i].append(location.latitude)
                    questions[i].append(location.longitude)
                else:
                    questions[i].append("None")
                    questions[i].append("None")
            else:
                questions[i].append("None")
                questions[i].append("None")
            one_tag = ""
            for separated_tag in questions[i][0]:
                if separated_tag == "python-3.x" or separated_tag == "python-2.7" or separated_tag == "python-3.6" or separated_tag == "python-3.7" or separated_tag == "python-3.8":
                    one_tag = one_tag + " " + "python" + " "
                elif separated_tag == "angular5" or separated_tag == "angular9" or separated_tag == "angular10":
                    one_tag = one_tag + " " + "angular" + " "
                elif separated_tag == "swiftui" or separated_tag == "swift2":
                    one_tag = one_tag + " " + "swift" + " "
                elif separated_tag == "sql-server-2008" or separated_tag == "sql-server-2005" or separated_tag == "sql-server-2012":
                    one_tag = one_tag + " " + "sql-server" + " "
                elif separated_tag == "ios7" or separated_tag == "ios13":
                    one_tag = one_tag + " " + "ios" + " "
                elif separated_tag == "vue-chartjs" or separated_tag == "vuejs2" or separated_tag == "vue-component" or separated_tag == "vue-router" or separated_tag == "vue-tables-2" or separated_tag == "vuetify.js" or separated_tag == "vuex":
                    one_tag = one_tag + " " + "vue.js" + " "
                elif separated_tag == "tensorflow2.0" or separated_tag == "tensorflow2.x":
                    one_tag = one_tag + " " + "tensorflow" + " "
                elif separated_tag == "postgresql-9.5" or separated_tag == "postgresql-9.6":
                    one_tag = one_tag + " " + "postgresql" + " "
                elif separated_tag == "xcode6" or separated_tag == "xcode11":
                    one_tag = one_tag + " " + "xcode" + " "
                elif separated_tag == "ruby-on-rails-5" or separated_tag == "ruby-on-rails-4" or separated_tag == "ruby-on-rails-3":
                    one_tag = one_tag + " " + "ruby-on-rails" + " "
                elif separated_tag == "laravel-5":
                    one_tag = one_tag + " " + "laravel" + " "
                elif separated_tag == "windows-10":
                    one_tag = one_tag + " " + "windows" + " "
                elif separated_tag == "visual-studio-2015" or separated_tag == "visual-studio-2019":
                    one_tag = one_tag + " " + "visual-studio" + " "
                elif separated_tag == "ionic5" or separated_tag == "ionic2" or separated_tag == "ionic4":
                    one_tag = one_tag + " " + "ionic-framework" + " "
                elif separated_tag == "f#-3.0":
                    one_tag = one_tag + " " + "f#" + " "
                elif separated_tag == "hadoop3":
                    one_tag = one_tag + " " + "hadoop" + " "
                elif separated_tag == "ubuntu-20.04" or separated_tag == "ubuntu-14.04":
                    one_tag = one_tag + " " + "ubuntu" + " "
                elif separated_tag == "fortran90":
                    one_tag = one_tag + " " + "fortran" + " "
                elif separated_tag == "drupal-7":
                    one_tag = one_tag + " " + "drupal" + " "
                elif separated_tag == "spring-boot":
                    one_tag = one_tag + " " + "spring" + " "
                elif separated_tag == "gitlab-ci":
                    one_tag = one_tag + " " + "gitlab" + " "
                elif separated_tag == "azure-devops":
                    one_tag = one_tag + " " + "azure" + " "
                elif separated_tag == "unity3d":
                    one_tag = one_tag + " " + "unity" + " "
                elif separated_tag == "unreal-engine4":
                    one_tag = one_tag + " " + "unreal-engine" + " "
                elif separated_tag == "sql-insert" or separated_tag == "sql-like":
                    one_tag = one_tag + " " + "sql" + " "
                elif separated_tag == "pandas-bokeh" or separated_tag == "pandas-groupby" or separated_tag == "pandas-resample":
                    one_tag = one_tag + " " + "pandas" + " "
                elif separated_tag == "html-agility-pack" or separated_tag == "html-parsing" or separated_tag == "html-table" or separated_tag == "html-webpack-plugin":
                    one_tag = one_tag + " " + "html" + " "
                else:
                    one_tag = one_tag + " " + separated_tag
            questions[i][0] = one_tag
            print(questions[i])
            processed_ids.append(i)
    final = pd.DataFrame.from_dict(questions, orient='index')
    colnames = ['Id','Tags','Timestamp','Votes','Answers','User ID','Title','Views','First Answer','Code','Comments',
                'Closed','Body','Location','Deleted','Latitude','Longitude']
    final.columns = colnames
    list_of_dataframes.append(final)


    print('Completed data extraction for {}'.format(tag))

df_final = pd.concat(list_of_dataframes, ignore_index = True)
df_final = df_final.drop_duplicates(subset=['Id'])
title = []
question_id = []
tags = []
first_answers = []
timestamps = []
votes = []
owner_id = []
views = []
body = []
location = []
latitude = []
longitude = []
tag = []
code_snippet = []
comments = []
answers = []
closed = []
deleted = []
tag_combinations = []
for index, row in df_final.iterrows():
    #edo prepei na ginei i problepsi kai an to label einai 1 na to bazei mesa allios oxi
    if row['Filter'] == 1:
        title.append(row['Title'])
        question_id.append(row['Id'])
        timestamps.append(row['Timestamp'])
        votes.append(row['Votes'])
        owner_id.append(row['User ID'])
        views.append(row['Views'])
        body.append(row['Body'])
        location.append(row['Location'])
        latitude.append(row['Latitude'])
        longitude.append(row['Longitude'])
        tag.append(row['Tags'])
        code_snippet.append(row['Code'])
        comments.append(row['Comments'])
        answers.append(row['Answers'])
        closed.append(row['Closed'])
        deleted.append(row['Deleted'])
        first_answers.append(row['First Answer'])
        if tags[0] == '[':
            tag_list = ast.literal_eval(tags)
            tag_list = [n.strip() for n in tag_list]
        else:
            tag_list = tags.split()
        for i in range(0, len(tag_list)):
            if tag_list[i] == "python-3.x" or tag_list[i] == "python-2.7" or tag_list[i] == "python-3.6" or \
                    tag_list[i] == "python-3.7" or tag_list[i] == "python-3.8":
                tag_list[i] = "python"
            elif tag_list[i] == "angular5" or tag_list[i] == "angular9" or tag_list[i] == "angular10":
                tag_list[i] = "angular"
            elif tag_list[i] == "swiftui" or tag_list[i] == "swift2":
                tag_list[i] = "swift"
            elif tag_list[i] == "sql-server-2008" or tag_list[i] == "sql-server-2005" or tag_list[
                i] == "sql-server-2012":
                tag_list[i] = "sql-server"
            elif tag_list[i] == "ios7" or tag_list[i] == "ios13":
                tag_list[i] = "ios"
            elif tag_list[i] == "vue-chartjs" or tag_list[i] == "vuejs2" or tag_list[i] == "vue-component" or \
                    tag_list[i] == "vue-router" or tag_list[i] == "vue-tables-2" or tag_list[i] == "vuetify.js" or \
                    tag_list[i] == "vuex":
                tag_list[i] = "vue.js"
            elif tag_list[i] == "tensorflow2.0" or tag_list[i] == "tensorflow2.x":
                tag_list[i] = "tensorflow"
            elif tag_list[i] == "postgresql-9.5" or tag_list[i] == "postgresql-9.6":
                tag_list[i] = "postgresql"
            elif tag_list[i] == "xcode6" or tag_list[i] == "xcode11":
                tag_list[i] = "xcode"
            elif tag_list[i] == "ruby-on-rails-5" or tag_list[i] == "ruby-on-rails-4" or tag_list[
                i] == "ruby-on-rails-3":
                tag_list[i] = "ruby-on-rails"
            elif tag_list[i] == "laravel-5":
                tag_list[i] = "laravel"
            elif tag_list[i] == "windows-10":
                tag_list[i] = "windows"
            elif tag_list[i] == "visual-studio-2015" or tag_list[i] == "visual-studio-2019":
                tag_list[i] = "visual-studio"
            elif tag_list[i] == "ionic5" or tag_list[i] == "ionic2" or tag_list[i] == "ionic4":
                tag_list[i] = "ionic-framework"
            elif tag_list[i] == "f#-3.0":
                tag_list[i] = "f#"
            elif tag_list[i] == "hadoop3":
                tag_list[i] = "hadoop"
            elif tag_list[i] == "ubuntu-20.04" or tag_list[i] == "ubuntu-14.04":
                tag_list[i] = "ubuntu"
            elif tag_list[i] == "fortran90":
                tag_list[i] = "fortran"
            elif tag_list[i] == "drupal-7":
                tag_list[i] = "drupal"
            elif tag_list[i] == "spring-boot":
                tag_list[i] = "spring"
            elif tag_list[i] == "gitlab-ci":
                tag_list[i] = "gitlab"
            elif tag_list[i] == "azure-devops":
                tag_list[i] = "azure"
            elif tag_list[i] == "unity3d":
                tag_list[i] = "unity"
            elif tag_list[i] == "unreal-engine4":
                tag_list[i] = "unreal-engine"
            elif tag_list[i] == "sql-insert" or tag_list[i] == "sql-like":
                tag_list[i] = "sql"
            elif tag_list[i] == "pandas-bokeh" or tag_list[i] == "pandas-groupby" or tag_list[
                i] == "pandas-resample":
                tag_list[i] = "pandas"
            elif tag_list[i] == "html-agility-pack" or tag_list[i] == "html-parsing" or tag_list[
                i] == "html-table" or tag_list[i] == "html-webpack-plugin":
                tag_list[i] = "html"
            else:
                tag_list[i] = tag_list[i]

        combinations = list(itertools.combinations(tag_list, 2))
        tag_combinations.append(combinations)

cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]
last = db.questions.find().sort('_id', pymongo.DESCENDING).limit(1)[0]['_id'] + 1
for i in range(len(title)):
    print(last + i)
    db.questions.insert_one({

        "_id": int(last + i),

        "timestamps": timestamps[i],

        "owner_id": owner_id[i],

        "votes": votes[i],

        "views": views[i],

        "question_id": question_id[i],

        "question_body": body[i],

        "question_title": title[i],

        "location": location[i],

        "latitude": latitude[i],

        "longitude": longitude[i],

        "tag": tag[i],

        "code_snippet": code_snippet[i],

        "comments": comments[i],

        "answers": answers[i],

        "closed": closed[i],

        "first_answer": first_answers[i] ,

        "filter": 1,

        "deleted": deleted[i]
    })
    if not combinations:
        collection.update_one(
            {"question_id": question_id[i]},
            {"$set":
                {
                    "tag_combinations": 'No tag combinations'
                }
            }
        )
    else:
        collection.update_one(
            {"question_id": question_id[i]},
            {"$set":
                {
                    "tag_combinations": combinations
                }
            }
        )

