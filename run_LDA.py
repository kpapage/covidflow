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
import ast
import itertools

cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]
questions = collection.find()

for question in questions:
    tags = question['tag']
    print(tags)
    if tags[0] == '[':
        tag_list = ast.literal_eval(tags)
        tag_list = [n.strip() for n in tag_list]
    else:
        tag_list = tags.split()
    for i in range(0,len(tag_list)):
        if tag_list[i] == "python-3.x" or tag_list[i] == "python-2.7" or tag_list[i] == "python-3.6" or tag_list[i] == "python-3.7" or tag_list[i] == "python-3.8":
            tag_list[i] = "python"
        elif tag_list[i] == "angular5" or tag_list[i] == "angular9" or tag_list[i] == "angular10":
            tag_list[i] = "angular"
        elif tag_list[i] == "swiftui" or tag_list[i] == "swift2":
            tag_list[i] = "swift"
        elif tag_list[i] == "sql-server-2008" or tag_list[i] == "sql-server-2005" or tag_list[i] == "sql-server-2012":
            tag_list[i] = "sql-server"
        elif tag_list[i] == "ios7" or tag_list[i] == "ios13":
            tag_list[i] = "ios"
        elif tag_list[i] == "vue-chartjs" or tag_list[i] == "vuejs2" or tag_list[i] == "vue-component" or tag_list[i] == "vue-router" or tag_list[i] == "vue-tables-2" or tag_list[i] == "vuetify.js" or tag_list[i] == "vuex":
            tag_list[i] = "vue.js"
        elif tag_list[i] == "tensorflow2.0" or tag_list[i] == "tensorflow2.x":
            tag_list[i] = "tensorflow"
        elif tag_list[i] == "postgresql-9.5" or tag_list[i] == "postgresql-9.6":
            tag_list[i] = "postgresql"
        elif tag_list[i] == "xcode6" or tag_list[i] == "xcode11":
            tag_list[i] = "xcode"
        elif tag_list[i] == "ruby-on-rails-5" or tag_list[i] == "ruby-on-rails-4" or tag_list[i] == "ruby-on-rails-3":
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
            tag_list[i] ="unity"
        elif tag_list[i] == "unreal-engine4":
            tag_list[i] = "unreal-engine"
        elif tag_list[i] == "sql-insert" or tag_list[i] == "sql-like":
            tag_list[i] = "sql"
        elif tag_list[i] == "pandas-bokeh" or tag_list[i] == "pandas-groupby" or tag_list[i] == "pandas-resample":
            tag_list[i] = "pandas"
        elif tag_list[i] == "html-agility-pack" or tag_list[i] == "html-parsing" or tag_list[i] == "html-table" or tag_list[i] == "html-webpack-plugin":
            tag_list[i] = "html"
        else:
            tag_list[i] = tag_list[i]

    combinations = list(itertools.combinations(tag_list, 2))
    if not combinations:
        collection.update_one(
            {"question_id": question['question_id']},
            {"$set":
                {
                    "tag_combinations":'No tag combinations'
                }
            }
        )
    else:
        collection.update_one(
            {"question_id": question['question_id']},
            {"$set":
                {
                    "tag_combinations": combinations
                }
            }
        )