def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def scrape_site_questions(tag):
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
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\giou2\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(
        executable_path='chromedriver_win32/chromedriver.exe'
        , options=options)
    searchdate = "2020-01-26..2022-12-8"
    print("Extracting question data about {}".format(tag))
    driver.get("https://stackoverflow.com/search?page=1&tab=Relevance&q={}%20created%3a{}%20{}%3a{}".format(tag, searchdate,'is','question'))
    results_text = driver.find_element(By.CSS_SELECTOR, ".flex--item.fl1.fs-body3.mr12").text
    numberOfResults = float(re.sub("[^0-9]", "", results_text))
    pages = math.ceil(numberOfResults / 15)
    print(pages)
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
                metadata.append(tag_list)
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
                time.sleep(1)
                questions[id] = metadata
                print(questions[id])
            for id in questions.keys():
                if id not in covered_ids:
                    split = id.split('-')
                    idd = split[2]
                    driver.get('https://stackoverflow.com/questions/{}'.format(idd))
                    time.sleep(2)
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
                        answers = driver.find_elements(By.XPATH, "//div[contains(@class, 'answercell')]")
                        timestamps = []
                        for answer in answers:
                            timestamp = answer.find_element(By.XPATH,"//span[contains(@class, 'relativetime')]")
                            timestamps.append(timestamp.get_attribute('title'))
                        if not timestamps:
                            questions[id].append('No answers')
                        if len(timestamps) == 1:
                            questions[id].append(timestamps[0])
                        else:
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
                    bodies = post.find_elements(By.XPATH,'//*[contains(@class,"js-post-body")]//descendant::p')
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
                    questions[id].append(0) #for deleted
        except NoSuchElementException:
            print('No questions in this page!')

        geoLocator = Nominatim(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
            timeout=3)
        for i in questions.keys():
            if i not in processed_ids:
                if (questions[i][11] != "No Location"):
                    location = geoLocator.geocode(questions[i][11])
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
                        one_tag = one_tag + " " + separated_tag + " "
                questions[i][0] = one_tag
                processed_ids.append(i)
        final = pd.DataFrame.from_dict(questions, orient='index')
        if tag == 'covid*':
            final.to_excel('collected_covid.xlsx')
        else:
            final.to_excel('collected_{}.xlsx'.format(tag))
    print('Completed data extraction for {}'.format(tag))

print('Extracting Question Data')
#
tags = ["sars-cov","2019-ncov","corona-virus","coronavirus","covid*"]

for tag in tags:
    scrape_site_questions(tag)
