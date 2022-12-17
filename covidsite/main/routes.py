from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from covidsite.extensions import mongo

from itertools import islice, combinations

from collections import Counter

import re

from datetime import datetime

import numpy as np

main = Blueprint('main', __name__)


@main.route('/',methods = ['GET','POST'])
def index():
    covidCollection = mongo.db.questions
    questions = covidCollection.find()  #load questions from collection
    questions = list(questions)
    closed_questions = list([q for q in questions if q['closed'] == 1])
    deleted_questions = list([q for q in questions if q['deleted'] == 1])
    all_questions = questions + closed_questions + deleted_questions





    techCollection = mongo.db.technologies_list
    technologies = techCollection.find()
    users = len(covidCollection.distinct('owner_id'))
    question_number = len(covidCollection.distinct('_id'))
    dates = []
    date_from = '2020-01-01'
    date_to = '2022-09-19'
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
    ids_and_votes = {}
    ids_and_answers = {}
    ids_and_comments = {}
    usernames = []
    locations = []
    location_name = []
    location_question = []
    languages = {}
    web_frameworks = {}
    big_data_ml = {}
    databases = {}
    platforms = {}
    collaboration_tools = {}
    dev_tools = {}

    fields_and_techs = {}
    for technology in technologies:
        fields_and_techs.update({technology['field'].lower():technology['technology']})

    question_count = 0
    for question in questions:
        question_count+=1
        dates.append(question['timestamps'][:10])
        record_tags = question['tag'].split()
        dif_tags = list(set(record_tags))

        if question['owner_id'] != 'No Owner ID':
            usernames.append(question['owner_id'])
        comments.append(question['comments'])
        answers.append(question['answers'])
        votes.append(int(question['votes']))
        q_id = question['question_id']
        q_link = "https://stackoverflow.com/questions/" + str(re.sub("[^0-9]", "",q_id))
        ids_and_votes.update({q_link :[ int(question['votes']),question['question_title']]})
        ids_and_answers.update({q_link: [int(question['answers']), question['question_title']]})
        ids_and_comments.update({q_link: [int(question['comments']), question['question_title']]})
        #########################
        for q_tag in dif_tags:
            if fields_and_techs.get(q_tag) == 'Languages':
                languages.update({q_link:[int(question['votes']),int(question['answers']),int(question['comments']),
                                          question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Web Frameworks':
                web_frameworks.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Big Data - ML':
                big_data_ml.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Databases':
                databases.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Platforms':
                platforms.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Collaboration Tools':
                collaboration_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Developer Tools':
                dev_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                                           question['question_title']]})
        #########################
        code_snippets.append(int(question['code_snippet']))
        if question['latitude'] != 'None':
            latLng =  [question['latitude'],question['longitude']]
            coordinates.append(latLng)
            latitudes.append(question['latitude'])
            longitudes.append(question['longitude'])
            locations.append(question['location'])
        for i in range(len(record_tags)):
            tags.append(record_tags[i])


    distinct_locations = Counter(locations)
    for key,value in distinct_locations.items():
        location_name.append(key)
        location_question.append(value)

    ############################
    sorted_language_votes=dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_languages_votes = dict(islice(sorted_language_votes.items(),10))

    sorted_language_answers = dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_languages_answers = dict(islice(sorted_language_answers.items(), 10))

    sorted_language_comments = dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_languages_comments = dict(islice(sorted_language_comments.items(), 10))



    sorted_web_frameworks_votes = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_web_frameworks_votes = dict(islice(sorted_web_frameworks_votes.items(), 10))

    sorted_web_frameworks_answers = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_web_frameworks_answers = dict(islice(sorted_web_frameworks_answers.items(), 10))

    sorted_web_frameworks_comments = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_web_frameworks_comments = dict(islice(sorted_web_frameworks_comments.items(), 10))


    sorted_big_data_ml_votes = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_big_data_ml_votes = dict(islice(sorted_big_data_ml_votes.items(), 10))

    sorted_big_data_ml_answers = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_big_data_ml_answers = dict(islice(sorted_big_data_ml_answers.items(), 10))

    sorted_big_data_ml_comments = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_big_data_ml_comments = dict(islice(sorted_big_data_ml_comments.items(), 10))


    sorted_databases_votes = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_databases_votes = dict(islice(sorted_databases_votes.items(), 10))

    sorted_databases_answers = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_databases_answers = dict(islice(sorted_databases_answers.items(), 10))

    sorted_databases_comments = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_databases_comments = dict(islice(sorted_databases_comments.items(), 10))


    sorted_platforms_votes = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_platforms_votes = dict(islice(sorted_platforms_votes.items(), 10))

    sorted_platforms_answers = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_platforms_answers = dict(islice(sorted_platforms_answers.items(), 10))

    sorted_platforms_comments = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_platforms_comments = dict(islice(sorted_platforms_comments.items(), 10))


    sorted_collaboration_tools_votes = dict(sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_collaboration_tools_votes = dict(islice(sorted_collaboration_tools_votes.items(), 10))

    sorted_collaboration_tools_answers = dict(sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_collaboration_tools_answers = dict(islice(sorted_collaboration_tools_answers.items(), 10))

    sorted_collaboration_tools_comments = dict(sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_collaboration_tools_comments = dict(islice(sorted_collaboration_tools_comments.items(), 10))

    ##############################################

    sorted_dev_tools_votes = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_dev_tools_votes = dict(islice(sorted_dev_tools_votes.items(), 10))

    sorted_dev_tools_answers = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_dev_tools_answers = dict(islice(sorted_dev_tools_answers.items(), 10))

    sorted_dev_tools_comments = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_dev_tools_comments = dict(islice(sorted_dev_tools_comments.items(), 10))


    distinct_users = Counter(usernames)
    sorted_distinct_users = dict(sorted(distinct_users.items(), reverse=True, key=lambda item: item[1]))
    top_10_distinct_users = dict(islice(sorted_distinct_users.items(),10))


    sorted_ids_and_votes= dict(
        sorted(ids_and_votes.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_votes = dict(islice(sorted_ids_and_votes.items(),10))

    sorted_ids_and_answers = dict(
        sorted(ids_and_answers.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_answers = dict(islice(sorted_ids_and_answers.items(), 10))

    sorted_ids_and_comments = dict(
        sorted(ids_and_comments.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_comments = dict(islice(sorted_ids_and_comments.items(), 10))

    numberOfComments = sum(comments)
    avgNumberOfComments = format((numberOfComments/question_number),'.3f')
    numberOfAnswers = sum(answers)
    avgNumberOfAnswers = format((numberOfAnswers/question_number),'.3f')
    numberOfVotes = sum(votes)
    avgNumberOfVotes = format((numberOfVotes / question_number), '.3f')
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
    top_ten_tags = list(top_ten_tags_and_values_barchart.keys()) # to 10 tag names for the chord diagram
        

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




    distinct_tags = []
    radar_values = [0,0,0,0,0,0,0] #[languages,frameworks,big data,dbs,platforms,collab tools,dev tools]
    stacked_open_values = [0,0,0,0,0,0,0] #[languages,frameworks,big data,dbs,platforms,collab tools,dev tools]
    stacked_closed_values = [0,0,0,0,0,0,0] #[languages,frameworks,big data,dbs,platforms,collab tools,dev tools]





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

    #Creation of the stacked bar chart values.
    for question in questions:
        if question['closed'] == 1:
            for tag in question['tag'].split(' '):
                if tag in fields_and_techs.keys():
                    if fields_and_techs.get(tag) == 'Languages':
                        stacked_closed_values[0] = stacked_closed_values[0] + 1
                    elif fields_and_techs.get(tag) == 'Web Frameworks':
                        stacked_closed_values[1] = stacked_closed_values[1] + 1
                    elif fields_and_techs.get(tag) == 'Big Data - ML':
                        stacked_closed_values[2] = stacked_closed_values[2] + 1
                    elif fields_and_techs.get(tag) == 'Databases':
                        stacked_closed_values[3] = stacked_closed_values[3] + 1
                    elif fields_and_techs.get(tag) == 'Platforms':
                        stacked_closed_values[4] = stacked_closed_values[4] + 1
                    elif fields_and_techs.get(tag) == 'Collaboration Tools':
                        stacked_closed_values[5] = stacked_closed_values[5] + 1
                    elif fields_and_techs.get(tag) == 'Developer Tools':
                        stacked_closed_values[6] = stacked_closed_values[6] + 1
        else:
            for tag in question['tag'].split(' '):
                if tag in fields_and_techs.keys():
                    if fields_and_techs.get(tag) == 'Languages':
                        stacked_open_values[0] = stacked_open_values[0] + 1
                    elif fields_and_techs.get(tag) == 'Web Frameworks':
                        stacked_open_values[1] = stacked_open_values[1] + 1
                    elif fields_and_techs.get(tag) == 'Big Data - ML':
                        stacked_open_values[2] = stacked_open_values[2] + 1
                    elif fields_and_techs.get(tag) == 'Databases':
                        stacked_open_values[3] = stacked_open_values[3] + 1
                    elif fields_and_techs.get(tag) == 'Platforms':
                        stacked_open_values[4] = stacked_open_values[4] + 1
                    elif fields_and_techs.get(tag) == 'Collaboration Tools':
                        stacked_open_values[5] = stacked_open_values[5] + 1
                    elif fields_and_techs.get(tag) == 'Developer Tools':
                        stacked_open_values[6] = stacked_open_values[6] + 1


    # Distinct technologies
    distinct_technologies = []
    for tech in fields_and_techs.values():
        if tech not in distinct_technologies:
            distinct_technologies.append(tech)





    #creation of chord diagram matrix
    tag_link_matrix = np.zeros((10,10)).astype(int)
    tags_to_be_linked = []

    for question in questions:
        record_tags = question['tag'].split()
        if [i for i in top_ten_tags if i in record_tags] :
            for tag in record_tags:
                if tag in top_ten_tags:
                    tags_to_be_linked.append(top_ten_tags.index(tag))
            if len(tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(tags_to_be_linked,2))
                for combination in combinations_of_tags:
                    if combination[0]!= combination[1]:
                        tag_link_matrix[combination[0],combination[1]] += 1
                        tag_link_matrix[combination[1],combination[0]] += 1
            tags_to_be_linked.clear()
    
    list_tag_link_matrix = np.array2string(tag_link_matrix, separator=",")

    return render_template('index.html', questions=questions, question_count = question_count, users=users, labels=labels, values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues,latLngInt=latLngInt,latitudes=latitudes,longitudes=longitudes,
                           distinct_technologies= distinct_technologies,
                           stacked_open_values=stacked_open_values,stacked_closed_values=stacked_closed_values,
                           radar_values=radar_values,added_values=added_values,avgNumberOfAnswers=avgNumberOfAnswers,
                           avgNumberOfComments=avgNumberOfComments,avgNumberOfVotes=avgNumberOfVotes,
                           snippetData=snippetData,halfMonthValues=halfMonthValues,
                           top_10_sorted_ids_and_votes = top_10_sorted_ids_and_votes,
                           top_10_sorted_ids_and_answers = top_10_sorted_ids_and_answers,
                           top_10_sorted_ids_and_comments = top_10_sorted_ids_and_comments,
                           top_10_distinct_users = top_10_distinct_users, location_name = location_name,
                           location_question= location_question,locations = locations,top_10_languages_votes = top_10_languages_votes,
                           top_10_languages_answers = top_10_languages_answers,top_10_languages_comments = top_10_languages_comments,
                           top_10_web_frameworks_votes = top_10_web_frameworks_votes,top_10_web_frameworks_answers = top_10_web_frameworks_answers,
                           top_10_web_frameworks_comments= top_10_web_frameworks_comments,top_10_big_data_ml_votes = top_10_big_data_ml_votes,
                           top_10_big_data_ml_answers=top_10_big_data_ml_answers,top_10_big_data_ml_comments = top_10_big_data_ml_comments,
                           top_10_databases_votes =top_10_databases_votes,top_10_databases_answers = top_10_databases_answers,
                           top_10_databases_comments = top_10_databases_comments,top_10_platforms_votes = top_10_platforms_votes,
                           top_10_platforms_answers = top_10_platforms_answers, top_10_platforms_comments = top_10_platforms_comments,
                           top_10_collaboration_tools_votes = top_10_collaboration_tools_votes,top_10_collaboration_tools_answers = top_10_collaboration_tools_answers,
                           top_10_collaboration_tools_comments = top_10_collaboration_tools_comments,top_10_dev_tools_votes = top_10_dev_tools_votes,
                           top_10_dev_tools_answers = top_10_dev_tools_answers,top_10_dev_tools_comments = top_10_dev_tools_comments,
                           date_from = date_from, date_to = date_to, list_tag_link_matrix = list_tag_link_matrix, top_ten_tags = top_ten_tags
                           )

@main.route('/get_lda')
def get_map():
    return render_template('lda_PCI_9_Topics_Titles.html')

@main.route('/get_dates', methods=['GET'])
def fetch():
    covidCollection = mongo.db.questions
    date_from = request.args.get('dateFrom')
    date_to = request.args.get('dateTo')
    closed = int(request.args.get('inclClosed'))
    # 'closed': {'$in': [0 , closed]} OR 'deleted': {'$in': [0 , closed]}
    questions = covidCollection.find({'timestamps': {'$gte' : date_from, '$lte' : date_to}  , 'closed': {'$in': [0 , closed]} , 'deleted': {'$in': [0 , closed]} })
    techCollection = mongo.db.technologies_list
    technologies = techCollection.find()
    users = len(questions.distinct('owner_id'))
    question_number = len(covidCollection.distinct('_id'))
    questions = list(questions)
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
    ids_and_votes = {}
    ids_and_answers = {}
    ids_and_comments = {}
    usernames = []
    locations = []
    location_name = []
    location_question = []
    languages = {}
    web_frameworks = {}
    big_data_ml = {}
    databases = {}
    platforms = {}
    collaboration_tools = {}
    dev_tools = {}

    fields_and_techs = {}
    for technology in technologies:
        fields_and_techs.update({technology['field'].lower(): technology['technology']})

    question_count = 0
    for question in questions:
        question_count+=1
        dates.append(question['timestamps'][:10])
        record_tags = question['tag'].split()
        dif_tags = list(set(record_tags))

        if question['owner_id'] != 'No Owner ID':
            usernames.append(question['owner_id'])
        comments.append(question['comments'])
        answers.append(question['answers'])
        votes.append(int(question['votes']))
        q_id = question['question_id']
        q_link = "https://stackoverflow.com/questions/" + str(re.sub("[^0-9]", "", q_id))
        ids_and_votes.update({q_link: [int(question['votes']), question['question_title']]})
        ids_and_answers.update({q_link: [int(question['answers']), question['question_title']]})
        ids_and_comments.update({q_link: [int(question['comments']), question['question_title']]})
        #########################
        for q_tag in dif_tags:
            if fields_and_techs.get(q_tag) == 'Languages':
                languages.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Web Frameworks':
                web_frameworks.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Big Data - ML':
                big_data_ml.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Databases':
                databases.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Platforms':
                platforms.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Collaboration Tools':
                collaboration_tools.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
            if fields_and_techs.get(q_tag) == 'Developer Tools':
                dev_tools.update(
                    {q_link: [int(question['votes']), int(question['answers']), int(question['comments']),
                              question['question_title']]})
        #########################
        code_snippets.append(int(question['code_snippet']))
        if question['latitude'] != 'None':
            latLng = [question['latitude'], question['longitude']]
            coordinates.append(latLng)
            latitudes.append(question['latitude'])
            longitudes.append(question['longitude'])
            locations.append(question['location'])
        for i in range(len(record_tags)):
            tags.append(record_tags[i])

    distinct_locations = Counter(locations)
    for key, value in distinct_locations.items():
        location_name.append(key)
        location_question.append(value)

    ############################
    sorted_language_votes = dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_languages_votes = dict(islice(sorted_language_votes.items(), 10))

    sorted_language_answers = dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_languages_answers = dict(islice(sorted_language_answers.items(), 10))

    sorted_language_comments = dict(sorted(languages.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_languages_comments = dict(islice(sorted_language_comments.items(), 10))

    sorted_web_frameworks_votes = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_web_frameworks_votes = dict(islice(sorted_web_frameworks_votes.items(), 10))

    sorted_web_frameworks_answers = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_web_frameworks_answers = dict(islice(sorted_web_frameworks_answers.items(), 10))

    sorted_web_frameworks_comments = dict(sorted(web_frameworks.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_web_frameworks_comments = dict(islice(sorted_web_frameworks_comments.items(), 10))

    sorted_big_data_ml_votes = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_big_data_ml_votes = dict(islice(sorted_big_data_ml_votes.items(), 10))

    sorted_big_data_ml_answers = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_big_data_ml_answers = dict(islice(sorted_big_data_ml_answers.items(), 10))

    sorted_big_data_ml_comments = dict(sorted(big_data_ml.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_big_data_ml_comments = dict(islice(sorted_big_data_ml_comments.items(), 10))

    sorted_databases_votes = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_databases_votes = dict(islice(sorted_databases_votes.items(), 10))

    sorted_databases_answers = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_databases_answers = dict(islice(sorted_databases_answers.items(), 10))

    sorted_databases_comments = dict(sorted(databases.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_databases_comments = dict(islice(sorted_databases_comments.items(), 10))

    sorted_platforms_votes = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_platforms_votes = dict(islice(sorted_platforms_votes.items(), 10))

    sorted_platforms_answers = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_platforms_answers = dict(islice(sorted_platforms_answers.items(), 10))

    sorted_platforms_comments = dict(sorted(platforms.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_platforms_comments = dict(islice(sorted_platforms_comments.items(), 10))

    sorted_collaboration_tools_votes = dict(
        sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_collaboration_tools_votes = dict(islice(sorted_collaboration_tools_votes.items(), 10))

    sorted_collaboration_tools_answers = dict(
        sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_collaboration_tools_answers = dict(islice(sorted_collaboration_tools_answers.items(), 10))

    sorted_collaboration_tools_comments = dict(
        sorted(collaboration_tools.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_collaboration_tools_comments = dict(islice(sorted_collaboration_tools_comments.items(), 10))

    ##############################################

    sorted_dev_tools_votes = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_dev_tools_votes = dict(islice(sorted_dev_tools_votes.items(), 10))

    sorted_dev_tools_answers = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][1]))
    top_10_dev_tools_answers = dict(islice(sorted_dev_tools_answers.items(), 10))

    sorted_dev_tools_comments = dict(
        sorted(dev_tools.items(), reverse=True, key=lambda item: item[1][2]))
    top_10_dev_tools_comments = dict(islice(sorted_dev_tools_comments.items(), 10))

    distinct_users = Counter(usernames)
    sorted_distinct_users = dict(sorted(distinct_users.items(), reverse=True, key=lambda item: item[1]))
    top_10_distinct_users = dict(islice(sorted_distinct_users.items(), 10))

    sorted_ids_and_votes = dict(
        sorted(ids_and_votes.items(), reverse=True, key=lambda item: item[1]))
    top_10_sorted_ids_and_votes = dict(islice(sorted_ids_and_votes.items(), 10))

    sorted_ids_and_answers = dict(
        sorted(ids_and_answers.items(), reverse=True, key=lambda item: item[1]))
    top_10_sorted_ids_and_answers = dict(islice(sorted_ids_and_answers.items(), 10))

    sorted_ids_and_comments = dict(
        sorted(ids_and_comments.items(), reverse=True, key=lambda item: item[1]))
    top_10_sorted_ids_and_comments = dict(islice(sorted_ids_and_comments.items(), 10))

    numberOfComments = sum(comments)
    avgNumberOfComments = format((numberOfComments / question_number), '.3f')
    numberOfAnswers = sum(answers)
    avgNumberOfAnswers = format((numberOfAnswers / question_number), '.3f')
    numberOfVotes = sum(votes)
    avgNumberOfVotes = format((numberOfVotes / question_number), '.3f')
    yesCounter = 0
    noCounter = 0
    for snippet in code_snippets:
        if snippet == 1:
            yesCounter += 1
        else:
            noCounter += 1

    snippetData = [yesCounter, noCounter]

    sorted_dates = sorted(dates, key=lambda d: tuple(map(int, d.split('-'))))

    for i in range(len(sorted_dates)):
        dates_and_values[sorted_dates[i]] = sorted_dates.count(sorted_dates[i])  # dict for the lineChart

    for i in range(len(tags)):
        tags_and_values[tags[i]] = tags.count(tags[i])  # dict for wordCloud

    sorted_tags_and_values = dict(
        sorted(tags_and_values.items(), reverse=True, key=lambda item: item[1]))  # sorted dict for wordCloud

    best_sorted_tags_and_values = dict(islice(sorted_tags_and_values.items(), 80))  # top 80 for wordCloud

    top_ten_tags_and_values_barchart = dict(islice(sorted_tags_and_values.items(), 10))  # top 10 for barChart
    top_ten_tags = list(top_ten_tags_and_values_barchart.keys()) # to 10 tag names for the chord diagram

    for key, value in best_sorted_tags_and_values.items():  # map the dict for the wordCloud
        d = {"text": key, "size": value}
        list_of_tags_and_values.append(d)

    labels = list(dates_and_values.keys())  # lineChart labels
    values = list(dates_and_values.values())  # lineChart values

    counter = 0
    days = 0
    previous_value = 0
    halfMonthValues = []
    for key, value in dates_and_values.items():
        counter += value
        if days == 7:
            difference = abs((counter / 7) - previous_value)
            for i in range(7):
                dummy = counter / 7
                if previous_value < dummy:
                    previous_value = previous_value + (difference / 7)
                    halfMonthValues.append(previous_value)
                else:
                    previous_value = previous_value - (difference / 7)
                    halfMonthValues.append(previous_value)
            counter = 0
            days = 0
        days += 1

    added_values = values.copy()

    for i in range(1, len(added_values)):
        added_values[i] = added_values[i] + added_values[i - 1]

    barChartLabels = list(top_ten_tags_and_values_barchart.keys())  # barChart labels
    barChartValues = list(top_ten_tags_and_values_barchart.values())  # barChart values

    list_of_tuples_for_coordinates = [tuple(elem) for elem in coordinates]

    coordinates_counter_dict = dict(Counter(list_of_tuples_for_coordinates))

    coordinates_latitude = []
    coordinates_longitude = []
    coordinates_values = []

    for key, value in coordinates_counter_dict.items():
        coordinates_latitude.append(key[0])
        coordinates_longitude.append(key[1])
        coordinates_values.append(value)

    normalized_coordinates_values = [float(i) / max(coordinates_values) for i in coordinates_values]

    latLngInt = []

    for i in range(len(coordinates_values)):
        latLngInt.append([coordinates_latitude[i], coordinates_longitude[i], normalized_coordinates_values[i]])

    distinct_tags = []
    radar_values = [0, 0, 0, 0, 0, 0, 0]  # [languages,frameworks,big data,dbs,platforms,collab tools,dev tools]
    stacked_open_values = [0, 0, 0, 0, 0, 0, 0]  # [languages,frameworks,big data,dbs,platforms,collab tools,dev tools]
    stacked_closed_values = [0, 0, 0, 0, 0, 0, 0]  # [languages,frameworks,big data,dbs,platforms,collab tools,dev tools]


    for tag in tags:
        if tag in fields_and_techs.keys():
            if tag not in distinct_tags:
                distinct_tags.append(tag)

    for tag in distinct_tags:
        if fields_and_techs.get(tag) == 'Languages':
            radar_values[0] = radar_values[0] + 1
        elif fields_and_techs.get(tag) == 'Web Frameworks':
            radar_values[1] = radar_values[1] + 1
        elif fields_and_techs.get(tag) == 'Big Data - ML':
            radar_values[2] = radar_values[2] + 1
        elif fields_and_techs.get(tag) == 'Databases':
            radar_values[3] = radar_values[3] + 1
        elif fields_and_techs.get(tag) == 'Platforms':
            radar_values[4] = radar_values[4] + 1
        elif fields_and_techs.get(tag) == 'Collaboration Tools':
            radar_values[5] = radar_values[5] + 1
        elif fields_and_techs.get(tag) == 'Developer Tools':
            radar_values[6] = radar_values[6] + 1

    for i in range(len(radar_values)):
        radar_values[i] = radar_values[i] / len(distinct_tags)

    # Creation of the stacked bar chart values.
    for question in questions:
        if question['closed'] == 1:
            for tag in question['tags']:
                if tag in fields_and_techs.keys():
                    if fields_and_techs.get(tag) == 'Languages':
                        stacked_closed_values[0] = stacked_closed_values[0] + 1
                    elif fields_and_techs.get(tag) == 'Web Frameworks':
                        stacked_closed_values[1] = stacked_closed_values[1] + 1
                    elif fields_and_techs.get(tag) == 'Big Data - ML':
                        stacked_closed_values[2] = stacked_closed_values[2] + 1
                    elif fields_and_techs.get(tag) == 'Databases':
                        stacked_closed_values[3] = stacked_closed_values[3] + 1
                    elif fields_and_techs.get(tag) == 'Platforms':
                        stacked_closed_values[4] = stacked_closed_values[4] + 1
                    elif fields_and_techs.get(tag) == 'Collaboration Tools':
                        stacked_closed_values[5] = stacked_closed_values[5] + 1
                    elif fields_and_techs.get(tag) == 'Developer Tools':
                        stacked_closed_values[6] = stacked_closed_values[6] + 1
        else:
            for tag in question['tags']:
                if tag in fields_and_techs.keys():
                    if fields_and_techs.get(tag) == 'Languages':
                        stacked_open_values[0] = stacked_open_values[0] + 1
                    elif fields_and_techs.get(tag) == 'Web Frameworks':
                        stacked_open_values[1] = stacked_open_values[1] + 1
                    elif fields_and_techs.get(tag) == 'Big Data - ML':
                        stacked_open_values[2] = stacked_open_values[2] + 1
                    elif fields_and_techs.get(tag) == 'Databases':
                        stacked_open_values[3] = stacked_open_values[3] + 1
                    elif fields_and_techs.get(tag) == 'Platforms':
                        stacked_open_values[4] = stacked_open_values[4] + 1
                    elif fields_and_techs.get(tag) == 'Collaboration Tools':
                        stacked_open_values[5] = stacked_open_values[5] + 1
                    elif fields_and_techs.get(tag) == 'Developer Tools':
                        stacked_open_values[6] = stacked_open_values[6] + 1

    # Distinct technologies
    distinct_technologies = []
    for tech in fields_and_techs.values():
        if tech not in distinct_technologies:
            distinct_technologies.append(tech)

    #creation of chord diagram matrix
    tag_link_matrix = np.zeros((10,10)).astype(int)
    tags_to_be_linked = []

    for question in questions:
        record_tags = question['tag'].split()
        if [i for i in top_ten_tags if i in record_tags] :
            for tag in record_tags:
                if tag in top_ten_tags:
                    tags_to_be_linked.append(top_ten_tags.index(tag))
            if len(tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(tags_to_be_linked,2))
                for combination in combinations_of_tags:
                    if combination[0]!= combination[1]:
                        tag_link_matrix[combination[0],combination[1]] += 1
                        tag_link_matrix[combination[1],combination[0]] += 1
            tags_to_be_linked.clear()
    
    list_tag_link_matrix = np.array2string(tag_link_matrix, separator=",")

    return render_template('index.html', questions=questions, question_count = question_count, users=users, labels=labels, values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues, latLngInt=latLngInt, latitudes=latitudes,
                           longitudes=longitudes,
                           distinct_technologies=distinct_technologies,
                           stacked_open_values=stacked_open_values, stacked_closed_values=stacked_closed_values,
                           radar_values=radar_values, added_values=added_values,
                           avgNumberOfAnswers=avgNumberOfAnswers,
                           avgNumberOfComments=avgNumberOfComments, avgNumberOfVotes=avgNumberOfVotes,
                           snippetData=snippetData, halfMonthValues=halfMonthValues,
                           top_10_sorted_ids_and_votes=top_10_sorted_ids_and_votes,
                           top_10_sorted_ids_and_answers=top_10_sorted_ids_and_answers,
                           top_10_sorted_ids_and_comments=top_10_sorted_ids_and_comments,
                           top_10_distinct_users=top_10_distinct_users, location_name=location_name,
                           location_question=location_question, locations=locations,
                           top_10_languages_votes=top_10_languages_votes,
                           top_10_languages_answers=top_10_languages_answers,
                           top_10_languages_comments=top_10_languages_comments,
                           top_10_web_frameworks_votes=top_10_web_frameworks_votes,
                           top_10_web_frameworks_answers=top_10_web_frameworks_answers,
                           top_10_web_frameworks_comments=top_10_web_frameworks_comments,
                           top_10_big_data_ml_votes=top_10_big_data_ml_votes,
                           top_10_big_data_ml_answers=top_10_big_data_ml_answers,
                           top_10_big_data_ml_comments=top_10_big_data_ml_comments,
                           top_10_databases_votes=top_10_databases_votes,
                           top_10_databases_answers=top_10_databases_answers,
                           top_10_databases_comments=top_10_databases_comments,
                           top_10_platforms_votes=top_10_platforms_votes,
                           top_10_platforms_answers=top_10_platforms_answers,
                           top_10_platforms_comments=top_10_platforms_comments,
                           top_10_collaboration_tools_votes=top_10_collaboration_tools_votes,
                           top_10_collaboration_tools_answers=top_10_collaboration_tools_answers,
                           top_10_collaboration_tools_comments=top_10_collaboration_tools_comments,
                           top_10_dev_tools_votes=top_10_dev_tools_votes,
                           top_10_dev_tools_answers=top_10_dev_tools_answers,
                           top_10_dev_tools_comments=top_10_dev_tools_comments, date_from = date_from, date_to = date_to,
                           list_tag_link_matrix = list_tag_link_matrix, top_ten_tags = top_ten_tags
                           )