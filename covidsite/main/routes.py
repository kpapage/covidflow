from flask import Blueprint, render_template

from covidsite.extensions import mongo

from itertools import islice

main = Blueprint('main', __name__)


@main.route('/')
def index():
    covidcollection = mongo.db.questions
    questions = covidcollection.find()
    users = len(covidcollection.distinct('owner_id'))

    dates = []
    dates_and_values = {}
    tags = []
    tags_and_values = {}
    list_of_tags_and_values = []
    for question in questions:
        dates.append(question['timestamps'][:10])
        record_tags = question['tags'].split()
        for i in range(len(record_tags)):
            tags.append(record_tags[i])

    sorted_dates = sorted(dates, key=lambda d: tuple(map(int, d.split('-'))))

    for i in range(len(sorted_dates)):
        dates_and_values[sorted_dates[i]] = sorted_dates.count(sorted_dates[i])

    for i in range(len(tags)):
        tags_and_values[tags[i]] = tags.count(tags[i])

    sorted_tags_and_values = dict(sorted(tags_and_values.items(), reverse=True, key=lambda item: item[1]))

    best_sorted_tags_and_values = dict(islice(sorted_tags_and_values.items(), 80))

    for key, value in best_sorted_tags_and_values.items():
        d = {"text": key, "size": value}
        list_of_tags_and_values.append(d)

    labels = list(dates_and_values.keys())
    values = list(dates_and_values.values())

    return render_template('index.html', questions=questions, users=users, labels=labels, values=values,
                           list_of_tags_and_values=list_of_tags_and_values)
