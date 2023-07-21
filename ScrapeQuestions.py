def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


import time
import re
import math
import itertools
from datetime import date, timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, roc_curve, auc, roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import ADASYN
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns
from keras.utils import pad_sequences
import tensorflow as tf
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
from xgboost import XGBClassifier
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import pymongo
from geopy.geocoders import Nominatim



METRICS = [
    tf.keras.metrics.AUC(name='roc-auc'),
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name="recall")
          ]

def create_embeddings_sentence_transformers(model, corpus):

    model = SentenceTransformer(model)


    embdeddings = model.encode(corpus, show_progress_bar=True)

    return embdeddings

def create_embeddings_bert(model, corpus):

    # Create a BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained(model)

    # Tokenize the corpus using BERT tokenizer and add special tokens
    tokenized_corpus = [tokenizer.encode(sent, add_special_tokens=True, max_length=512, truncation=True) for sent in corpus]

    # Pad tokenized corpus to a fixed length of 512 tokens
    X = pad_sequences(tokenized_corpus, maxlen=512, dtype='int32', padding='post', truncating='post', value=0)

    return X

def encode_BERT_2(model, corpus):

    tokenizer = BertTokenizer.from_pretrained(model)
    encoded_dict = tokenizer.batch_encode_plus(corpus, add_special_tokens=True, max_length=128, padding='max_length',
                                               return_attention_mask=True, truncation=True, return_tensors='pt')
    input_ids = encoded_dict['input_ids']
    attention_masks = encoded_dict['attention_mask']
    return input_ids, attention_masks


def create_corpus2(X):
    corpus = []
    for i in range(0, len(X)):
        review = re.sub(r'[^a-zA-Z0-9\s]', '', X[i])
        review = re.sub(r'http\S+', '', review)

        review = review.lower()
        words = word_tokenize(review)
        tagged = pos_tag(words)
        chunked = ne_chunk(tagged)
        filtered = [tup[0] for tup in tagged if
                    (tup[1].startswith("N") or tup[1].startswith("V") or tup[1].startswith("J"))]
        corpus.append(' '.join(filtered))

    return corpus


def create_corpus(X):

    # Create a corpus
    corpus = []
    for i in range(0, len(X)):
        review = re.sub(r'[^a-zA-Z0-9\s]', '', X[i])
        review = re.sub(r'http\S+', '', review)

        review = review.lower()
        review = review.split()
        ps = WordNetLemmatizer()
        review = [ps.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)

    return corpus

def load_prepare_data(dir, test_size=0.2):

    # Importing the dataset
    df = pd.read_excel(dir, engine='openpyxl')
    #Convert the columns to strings
    df['Title'] = df['Title'].values.astype(str)
    df['Body'] = df['Body'].values.astype(str)

    # extract the title and body columns as the input data and combine them into a single column
    X = df['Title'] + ' ' + df['Body']

    # extract the class column as the target data
    y = df["Filter"].values

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    #X_train as ndarray
    X_train = X_train.to_numpy()
    #X_test as ndarray
    X_test = X_test.to_numpy()

    train_corpus = create_corpus2(X_train)
    test_corpus = create_corpus2(X_test)

    # Create embeddings using BERT
   # X_train = create_embeddings_bert('bert-base-uncased', train_corpus)
    #X_test = create_embeddings_bert('bert-base-uncased', test_corpus)

    # Create embeddings using sentence_transformers
    X_train = create_embeddings_sentence_transformers('all-mpnet-base-v2', train_corpus)
    X_test = create_embeddings_sentence_transformers('all-mpnet-base-v2', test_corpus)

    # Create embeddings using BERT_2
    #train_input_ids, train_att_masks = encode_BERT_2('bert-base-uncased', train_corpus)
    #test_input_ids, test_att_masks = encode_BERT_2('bert-base-uncased', test_corpus)



    # Oversample the minority class using Borderline-SMOTE
    #b_smote = BorderlineSMOTE(random_state=42, n_jobs=-1)
    #X_train_resampled, y_train_resampled = b_smote.fit_resample(X_train, y_train)

    # Oversample the minority class using ADASYN
    adasyn = ADASYN(random_state=42, n_jobs=-1)
    X_train_resampled, y_train_resampled = adasyn.fit_resample(X_train, y_train)



    # Split the oversampled data into training and test sets
    return X_train_resampled, X_test, y_train_resampled, y_test


def print_metrics(y_test, y_pred):

    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Precision: ", precision_score(y_test, y_pred))
    print("Recall: ", recall_score(y_test, y_pred))
    print("F1 Score: ", f1_score(y_test, y_pred))

def show_roc_curve(y_test, y_pred):

    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    plt.plot(fpr, tpr, label='AUC-ROC = %0.2f' % auc(fpr, tpr))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('AUC-ROC Curve')
    plt.legend()
    plt.show()

def show_conf_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    sns.heatmap(cm, annot=True)
    plt.title('Confusion matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()




def create_classifier():
    n_jobs = os.cpu_count() - 1
    if n_jobs is None:
        n_jobs = -1

    # Load and preprocess the data
    X_train, X_test, y_train, y_test = load_prepare_data('GroundTruth.xlsx', test_size=0.25)

    n_splits = 10
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Hold the metric scores for each fold
    acc_scores = []
    prec_scores = []
    rec_scores = []
    f1_scores = []
    auc_scores = []

    # X should be equal to X_train plus X_test
    X = np.concatenate((X_train, X_test), axis=0)
    y = np.concatenate((y_train, y_test), axis=0)

    for fold, (train_index, test_index) in enumerate(skf.split(X, y)):
        print(f"Fold {fold + 1}")

        # Split the data into training and test sets for this fold
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Train and evaluate the model for this fold
        model = XGBClassifier(n_estimators=1000, max_depth=10, n_jobs=n_jobs)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred)

        # Save the scores for this fold
        acc_scores.append(accuracy)
        prec_scores.append(precision)
        rec_scores.append(recall)
        f1_scores.append(f1)
        auc_scores.append(auc)

        # Print the scores for this fold
        print_metrics(y_test, y_pred)

    # Print the average scores across all folds
    print(f"Average accuracy: {np.mean(acc_scores)}")
    print(f"Average precision: {np.mean(prec_scores)}")
    print(f"Average recall: {np.mean(rec_scores)}")
    print(f"Average F1 score: {np.mean(f1_scores)}")
    print(f"Average AUC score: {np.mean(auc_scores)}")

    show_conf_matrix(y_test, y_pred)


classifier=pd.read_pickle("xgb_model.pkl")
options = FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=options)


labels = ['covid*', "coronavirus", "corona-virus", "2019-ncov", "sars-cov"]
with open("searchdate.txt") as file:
    searchdate = file.readline()

list_of_dataframes = []
for label in labels:
    print("Extracting question data about {}".format(label))
    driver.get("https://stackoverflow.com/search?page=1&tab=Relevance&q={}%20created%3a{}%20{}%3a{}".format(label, searchdate,'is','question'))
    results_text = driver.find_element(By.CSS_SELECTOR, ".flex--item.fl1.fs-body3.mr12").text
    numberOfResults = float(re.sub("[^0-9]", "", results_text))
    pages = math.ceil(numberOfResults / 15)
    questions = {}
    covered_ids = []
    processed_ids = []
    for i in range(pages):
        driver.get("https://stackoverflow.com/search?page={}&tab=Relevance&q={}%20created%3a{}%20{}%3a{}".format(i+1, label, searchdate,'is','question'))
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
                timestamp_list = driver.find_elements(By.XPATH,"//div[contains(@id, 'answer-')]//div[contains(@class, 'answercell')]//span[contains(@class, 'relativetime')]")
                time.sleep(5)
                timestamps = []
                for element in timestamp_list:
                    timestamps.append(element.get_attribute('title'))
                if not timestamps:
                    questions[id].append('No answers')
                if len(timestamps) == 1:
                    questions[id].append(timestamps[0])
                if len(timestamps) > 1:
                    first_answer = min(timestamps)
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
            processed_ids.append(i)
    final = pd.DataFrame.from_dict(questions, orient='index')
    final.reset_index(inplace=True)
    list_of_dataframes.append(final)
    print('Completed data extraction for {}'.format(label))

df_final = pd.concat(list_of_dataframes, ignore_index = True)
colnames = ['Id', 'Tags', 'Timestamp', 'Votes', 'Answers', 'User ID', 'Title', 'Views', 'First Answer', 'Code','Comments', 'Closed', 'Body', 'Location', 'Deleted', 'Latitude', 'Longitude']
df_final.columns = colnames
df_final = df_final.drop_duplicates(subset=['Id'])
print('Constructed Final Dataframe')
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
code_snippet = []
comments = []
answers = []
closed = []
deleted = []
tag_combinations = []

# Convert the columns to strings
df_final['Title'] = df_final['Title'].values.astype(str)
df_final['Body'] = df_final['Body'].values.astype(str)

# extract the title and body columns as the input data and combine them into a single column
X = df_final['Title'] + ' ' + df_final['Body']

corpus_X = create_corpus2(X)

X_embed = create_embeddings_sentence_transformers('all-mpnet-base-v2', corpus_X)

pred = classifier.predict(X_embed)
pred = pd.DataFrame(pred)
df_final['Filter'] = pred
print('Completed Filtering')
# extract the class column as the target data
# y = df["Filter"].values
for index, row in df_final.iterrows():
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
        tags.append(row['Tags'])
        code_snippet.append(row['Code'])
        comments.append(row['Comments'])
        answers.append(row['Answers'])
        closed.append(row['Closed'])
        deleted.append(row['Deleted'])
        first_answers.append(row['First Answer'])
        tag_list = row['Tags']
        tag_list = tag_list[1:]
        to_combine = []
        for tag in tag_list.split(' '):
            if tag == "python-3.x" or tag == "python-2.7" or tag == "python-3.6" or \
                    tag == "python-3.7" or tag == "python-3.8":
                tag = "python"
            elif tag == "angular5" or tag == "angular9" or tag == "angular10":
                tag = "angular"
            elif tag == "swiftui" or tag == "swift2":
                tag = "swift"
            elif tag == "sql-server-2008" or tag == "sql-server-2005" or tag == "sql-server-2012":
                tag = "sql-server"
            elif tag == "ios7" or tag == "ios13":
                tag = "ios"
            elif tag == "vue-chartjs" or tag == "vuejs2" or tag == "vue-component" or \
                    tag == "vue-router" or tag == "vue-tables-2" or tag == "vuetify.js" or \
                    tag == "vuex":
                tag = "vue.js"
            elif tag == "tensorflow2.0" or tag == "tensorflow2.x":
                tag = "tensorflow"
            elif tag == "postgresql-9.5" or tag == "postgresql-9.6":
                tag = "postgresql"
            elif tag == "xcode6" or tag == "xcode11":
                tag = "xcode"
            elif tag == "ruby-on-rails-5" or tag == "ruby-on-rails-4" or tag == "ruby-on-rails-3":
                tag = "ruby-on-rails"
            elif tag == "laravel-5":
                tag = "laravel"
            elif tag == "windows-10":
                tag = "windows"
            elif tag == "visual-studio-2015" or tag == "visual-studio-2019":
                tag = "visual-studio"
            elif tag == "ionic5" or tag == "ionic2" or tag == "ionic4":
                tag = "ionic-framework"
            elif tag == "f#-3.0":
                tag = "f#"
            elif tag == "hadoop3":
                tag = "hadoop"
            elif tag == "ubuntu-20.04" or tag == "ubuntu-14.04":
                tag = "ubuntu"
            elif tag == "fortran90":
                tag = "fortran"
            elif tag == "drupal-7":
                tag = "drupal"
            elif tag == "spring-boot":
                tag = "spring"
            elif tag == "gitlab-ci":
                tag = "gitlab"
            elif tag == "azure-devops":
                tag = "azure"
            elif tag == "unity3d":
                tag = "unity"
            elif tag == "unreal-engine4":
                tag = "unreal-engine"
            elif tag == "sql-insert" or tag == "sql-like":
                tag = "sql"
            elif tag == "pandas-bokeh" or tag == "pandas-groupby" or tag == "pandas-resample":
                tag = "pandas"
            elif tag == "html-agility-pack" or tag == "html-parsing" or tag == "html-table" or tag == "html-webpack-plugin":
                tag = "html"
            else:
                tag = tag
            to_combine.append(tag)
        combinations = list(itertools.combinations(to_combine, 2))
        tag_combinations.append(combinations)
print('Completed Combinations Extraction')
cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]
last = db.questions.find().sort('_id', pymongo.DESCENDING).limit(1)[0]['_id'] + 1
for i in range(len(title)):
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

        "tag": tags[i],

        "code_snippet": code_snippet[i],

        "comments": comments[i],

        "answers": answers[i],

        "closed": closed[i],

        "first_answer": first_answers[i] ,

        "filter": 1,

        "deleted": deleted[i]
    })
    if not tag_combinations:
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
                    "tag_combinations": tag_combinations[i]
                }
            }
        )
print('Completed Database Insertion')
today = date.today()
d = timedelta(days=7)
week = today + d
newsearchdate = str(today) + '...' + str(week)
print(newsearchdate)
with open('searchdate.txt', 'w') as f:
    f.write(newsearchdate)