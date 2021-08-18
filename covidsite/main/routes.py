from flask import Blueprint, render_template

from covidsite.extensions import mongo

from itertools import islice

from collections import Counter

main = Blueprint('main', __name__)


@main.route('/')
def index():
    covidCollection = mongo.db.questions
    questions = covidCollection.find()  #load questions from collection

    users = len(covidCollection.distinct('owner_id'))

    dates = []
    dates_and_values = {}
    tags = []
    tags_and_values = {}
    list_of_tags_and_values = []
    latitudes = []
    longitudes = []
    coordinates = []
    comments = []
    answers = []
    votes = []
    code_snippets = []
    added_values = []

    for question in questions:
        dates.append(question['timestamps'][:10])
        record_tags = question['tag'].split()
        comments.append(question['comments'])
        answers.append(question['answers'])
        votes.append(int(question['votes']))
        code_snippets.append(int(question['code_snippet']))
        if question['latitude'] != 'None':
            latLng =  [question['latitude'],question['longitude']]
            coordinates.append(latLng)
            latitudes.append(question['latitude'])
            longitudes.append(question['longitude'])
        for i in range(len(record_tags)):
            tags.append(record_tags[i])


    numberOfComments = sum(comments)
    avgNumberOfComments = format((numberOfComments/questions.count()),'.3f')
    numberOfAnswers = sum(answers)
    avgNumberOfAnswers = format((numberOfAnswers/questions.count()),'.3f')
    numberOfVotes = sum(votes)
    avgNumberOfVotes = format((numberOfVotes / questions.count()), '.3f')

    yesCounter = 0
    noCounter = 0
    for snippet in code_snippets:
        if snippet == 1:
            yesCounter+=1
        else:
            noCounter+=1

    snippetData = [yesCounter,noCounter]

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

    counter = 0
    days = 0
    previous_value = 0
    halfMonthValues = []
    for key,value in dates_and_values.items():
        counter+=value
        if days ==7:
            difference = abs((counter/7)-previous_value)
            for i in range(7):
                dummy = counter/7
                if previous_value < dummy:
                    previous_value=previous_value+(difference/7)
                    halfMonthValues.append(previous_value)
                else:
                    previous_value = previous_value - (difference/7)
                    halfMonthValues.append(previous_value)
            counter = 0
            days = 0
        days+=1


    added_values = values.copy()


    for i in range(1,len(added_values)):
        added_values[i]=added_values[i]+added_values[i-1]


    barChartLabels = list(top_ten_tags_and_values_barchart.keys())  # barChart labels
    barChartValues = list(top_ten_tags_and_values_barchart.values())  # barChart values

    list_of_tuples_for_coordinates=[tuple(elem) for elem in coordinates]

    coordinates_counter_dict = dict(Counter(list_of_tuples_for_coordinates))

    coordinates_latitude= []
    coordinates_longitude = []
    coordinates_values = []

    for key,value in coordinates_counter_dict.items():
        coordinates_latitude.append(key[0])
        coordinates_longitude.append(key[1])
        coordinates_values.append(value)

    normalized_coordinates_values = [float(i)/max(coordinates_values) for i in coordinates_values]

    latLngInt=[]

    for i in range(len(coordinates_values)):
        latLngInt.append([coordinates_latitude[i],coordinates_longitude[i],normalized_coordinates_values[i]])

    techCollection = mongo.db.technologies_list
    technologies = techCollection.find()

    fields_and_techs ={}
    distinct_tags = []
    radar_values = [0,0,0,0,0,0,0] #[languages,frameworks,big data,dbs,platforms,collab tools,dev tools]



    for technology in technologies:
        fields_and_techs.update({technology['field'].lower():technology['technology']})

    for tag in tags:
        if tag in fields_and_techs.keys():
            if tag not in distinct_tags:
                distinct_tags.append(tag)

    for tag in distinct_tags:
        if fields_and_techs.get(tag)== 'Languages':
            radar_values[0]=radar_values[0]+1
        elif fields_and_techs.get(tag)== 'Web Frameworks':
            radar_values[1] = radar_values[1] + 1
        elif fields_and_techs.get(tag)== 'Big Data - ML':
            radar_values[2] = radar_values[2] + 1
        elif fields_and_techs.get(tag)== 'Databases':
            radar_values[3] = radar_values[3] + 1
        elif fields_and_techs.get(tag)== 'Platforms':
            radar_values[4] = radar_values[4] + 1
        elif fields_and_techs.get(tag)== 'Collaboration Tools':
            radar_values[5] = radar_values[5] + 1
        elif fields_and_techs.get(tag)== 'Developer Tools':
            radar_values[6] = radar_values[6] + 1

    for i in range(len(radar_values)):
        radar_values[i]=radar_values[i]/len(distinct_tags)





    return render_template('index.html', questions=questions, users=users, labels=labels, values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues,latLngInt=latLngInt,latitudes=latitudes,longitudes=longitudes,
                           radar_values=radar_values,added_values=added_values,avgNumberOfAnswers=avgNumberOfAnswers,
                           avgNumberOfComments=avgNumberOfComments,avgNumberOfVotes=avgNumberOfVotes,
                           snippetData=snippetData,halfMonthValues=halfMonthValues)
