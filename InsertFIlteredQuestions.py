import openpyxl
import pandas as pd
import pymongo

title = []
question_id = []
tags = []
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
data = pd.read_excel('groundtruthEXTRA.xlsx')

for index, row in data.iterrows():
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

cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["COVID-db"]
collection = db["questions"]
last = db.questions.find().sort('_id', pymongo.DESCENDING).limit(1)[0]['_id'] + 1

for id in question_id:
    print(id)

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

        "first_answer": 'Not',

        "filter": 1,

        "deleted": deleted[i]
    })


