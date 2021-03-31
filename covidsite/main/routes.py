from flask import Blueprint, render_template

from covidsite.extensions import mongo

main = Blueprint('main', __name__)


@main.route('/')
def index():
    covidcollection = mongo.db.questions
    questions = covidcollection.find()
    users = len(covidcollection.distinct('owner_id'))

    dates = []
    dates_and_values = {}
    for question in questions:
        dates.append(question['timestamps'][:10])

    sorted_dates = sorted(dates, key=lambda d: tuple(map(int, d.split('-'))))

    for i in range(len(sorted_dates)):
        dates_and_values[sorted_dates[i]] = sorted_dates.count(sorted_dates[i])

    labels = list(dates_and_values.keys())
    values = list(dates_and_values.values())

    return render_template('index.html', questions=questions, users=users, labels=labels, values=values)
