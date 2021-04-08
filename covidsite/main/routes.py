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
    latitudes = []
    longitudes = []

    for question in questions:
        dates.append(question['timestamps'][:10])
        record_tags = question['tags'].split()
        if question['latitude'] != 'None':
            latitudes.append(question['latitude'])
            longitudes.append(question['longitude'])
        for i in range(len(record_tags)):
            tags.append(record_tags[i])

    sorted_dates = sorted(dates, key=lambda d: tuple(map(int, d.split('-'))))

    for i in range(len(sorted_dates)):
        dates_and_values[sorted_dates[i]] = sorted_dates.count(sorted_dates[i])  # dict for the lineChart

    for i in range(len(tags)):
        tags_and_values[tags[i]] = tags.count(tags[i])  # dict for wordCloud

    sorted_tags_and_values = dict(
        sorted(tags_and_values.items(), reverse=True, key=lambda item: item[1]))  # sorted dict for wordCloud

    best_sorted_tags_and_values = dict(islice(sorted_tags_and_values.items(), 80))  # top 80 for wordCloud

    top_ten_tags_and_values_barchart = dict(islice(sorted_tags_and_values.items(), 10))  # top 10 for barChart

    for key, value in best_sorted_tags_and_values.items():  # map the dict for the wordCloud
        d = {"text": key, "size": value}
        list_of_tags_and_values.append(d)

    labels = list(dates_and_values.keys())  # lineChart labels
    values = list(dates_and_values.values())  # lineChart values

    barChartLabels = list(top_ten_tags_and_values_barchart.keys())  # lineChart labels
    barChartValues = list(top_ten_tags_and_values_barchart.values())  # lineChart values

    for i in range(len(latitudes)):
        print(str(latitudes[i])+','+str(longitudes[i]))

    return render_template('index.html', questions=questions, users=users, labels=labels, values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues,latitudes=latitudes,longitudes=longitudes)
