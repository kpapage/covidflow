from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from covidsite.extensions import mongo

from itertools import islice, combinations

from collections import Counter

import re

from datetime import datetime

from datetime import timezone

import numpy as np

from operator import itemgetter

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    covidCollection = mongo.db.questions
    questions = covidCollection.find()  # load questions from collection
    all_questions = list(questions)
    closed_questions = list([q for q in all_questions if q['closed'] == 1])
    deleted_questions = list([q for q in all_questions if q['deleted'] == 1])
    questions = list([q for q in all_questions if q['closed'] == 0 and q['deleted'] == 0])



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
    elapsed_time_data_list = []
    languages_elapsed_time_data_list = []
    web_frameworks_elapsed_time_data_list = []
    big_data_ml_elapsed_time_data_list = []
    databases_elapsed_time_data_list = []
    platforms_elapsed_time_data_list = []
    collaboration_tools_elapsed_time_data_list = []
    dev_tools_elapsed_time_data_list = []

    fields_and_techs = {}
    for technology in technologies:
        fields_and_techs.update({technology['field'].lower(): technology['technology']})

    question_count = 0
    for question in questions:
        question_count += 1
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
        
        question_time = datetime.fromisoformat(question['timestamps'][:-1]).replace(tzinfo=timezone.utc)
        if question_time:           
            if question['first_answer'] != 'No answers':
                first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                event = 1   
            else:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                event = 0    
            if hour_diff!=0.0:
                elapsed_time_data_list.append([hour_diff,event])
        #########################
        for q_tag in dif_tags:
            if fields_and_techs.get(q_tag) == 'Languages':
                languages.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        languages_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Web Frameworks':
                web_frameworks.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        web_frameworks_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Big Data - ML':
                big_data_ml.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        big_data_ml_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Databases':
                databases.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        databases_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Platforms':
                platforms.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        platforms_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Collaboration Tools':
                collaboration_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        collaboration_tools_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Developer Tools':
                dev_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        dev_tools_elapsed_time_data_list.append([hour_diff,event])
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
    
    sorted_elapsed_time_data_list = sorted(elapsed_time_data_list, key=itemgetter(0))
    languages_sorted_elapsed_time_data_list = sorted(languages_elapsed_time_data_list, key=itemgetter(0))
    web_frameworks_sorted_elapsed_time_data_list = sorted(web_frameworks_elapsed_time_data_list, key=itemgetter(0))
    big_data_ml_sorted_elapsed_time_data_list = sorted(big_data_ml_elapsed_time_data_list, key=itemgetter(0))
    databases_sorted_elapsed_time_data_list = sorted(databases_elapsed_time_data_list, key=itemgetter(0))
    platforms_sorted_elapsed_time_data_list = sorted(platforms_elapsed_time_data_list, key=itemgetter(0))
    collaboration_tools_sorted_elapsed_time_data_list = sorted(collaboration_tools_elapsed_time_data_list, key=itemgetter(0))
    dev_tools_sorted_elapsed_time_data_list = sorted(dev_tools_elapsed_time_data_list, key=itemgetter(0))
    
    
    times_data_list = []
    number_of_distinct_times_data_list = []
    censored_data_list = []
    times_left_list = []
    
    item_counter = 1
    times_data_list.append(0)
    number_of_distinct_times_data_list.append(0)
    censored_data_list.append(0)
    times_left_list.append(len(sorted_elapsed_time_data_list))
    
    for item in sorted_elapsed_time_data_list:
        if item[0] not in times_data_list :
            if item[1] == 1:
                times_data_list.append(item[0])
                number_of_distinct_times_data_list.append(1)
                censored_data_list.append(0) 
                times_left_list.append(times_left_list[item_counter - 1] - (number_of_distinct_times_data_list[item_counter - 1] + censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                censored_data_list[item_counter-1]+=1
        
    survival_time_curve_values = []
    for i in range(len(times_data_list)):
        if i == 0:
            survival_time_curve_values.append((times_left_list[i] - number_of_distinct_times_data_list[i]) /  times_left_list[i])
        else:
            survival_time_curve_values.append(((times_left_list[i] - number_of_distinct_times_data_list[i]) /  times_left_list[i])* survival_time_curve_values[i-1])
    
    
    
    languages_times_data_list = []
    languages_number_of_distinct_times_data_list = []
    languages_censored_data_list = []
    languages_times_left_list = []

    item_counter = 1
    languages_times_data_list.append(0)
    languages_number_of_distinct_times_data_list.append(0)
    languages_censored_data_list.append(0)
    languages_times_left_list.append(len(languages_sorted_elapsed_time_data_list))

    for item in languages_sorted_elapsed_time_data_list:
        if item[0] not in languages_times_data_list :
            if item[1] == 1:
                languages_times_data_list.append(item[0])
                languages_number_of_distinct_times_data_list.append(1)
                languages_censored_data_list.append(0) 
                languages_times_left_list.append(languages_times_left_list[item_counter - 1] - (languages_number_of_distinct_times_data_list[item_counter - 1] + languages_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                languages_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                languages_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                languages_censored_data_list[item_counter-1]+=1

    languages_survival_time_curve_values = []
    for i in range(len(languages_times_data_list)):
        if i == 0:
            languages_survival_time_curve_values.append((languages_times_left_list[i] - languages_number_of_distinct_times_data_list[i]) /  languages_times_left_list[i])
        else:
            languages_survival_time_curve_values.append(((languages_times_left_list[i] - languages_number_of_distinct_times_data_list[i]) /  languages_times_left_list[i]) * languages_survival_time_curve_values[i-1])
        
    
    
    web_frameworks_times_data_list = []
    web_frameworks_number_of_distinct_times_data_list = []
    web_frameworks_censored_data_list = []
    web_frameworks_times_left_list = []

    item_counter = 1
    web_frameworks_times_data_list.append(0)
    web_frameworks_number_of_distinct_times_data_list.append(0)
    web_frameworks_censored_data_list.append(0)
    web_frameworks_times_left_list.append(len(web_frameworks_sorted_elapsed_time_data_list))

    for item in web_frameworks_sorted_elapsed_time_data_list:
        if item[0] not in web_frameworks_times_data_list :
            if item[1] == 1:
                web_frameworks_times_data_list.append(item[0])
                web_frameworks_number_of_distinct_times_data_list.append(1)
                web_frameworks_censored_data_list.append(0) 
                web_frameworks_times_left_list.append(web_frameworks_times_left_list[item_counter - 1] - (web_frameworks_number_of_distinct_times_data_list[item_counter - 1] + web_frameworks_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                web_frameworks_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                web_frameworks_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                web_frameworks_censored_data_list[item_counter-1]+=1
                
    web_frameworks_survival_time_curve_values = []
    for i in range(len(web_frameworks_times_data_list)):
        if i == 0:
            web_frameworks_survival_time_curve_values.append((web_frameworks_times_left_list[i] - web_frameworks_number_of_distinct_times_data_list[i]) /  web_frameworks_times_left_list[i])
        else:
            web_frameworks_survival_time_curve_values.append(((web_frameworks_times_left_list[i] - web_frameworks_number_of_distinct_times_data_list[i]) /  web_frameworks_times_left_list[i])* web_frameworks_survival_time_curve_values[i-1])
        
        

    big_data_ml_times_data_list = []
    big_data_ml_number_of_distinct_times_data_list = []
    big_data_ml_censored_data_list = []
    big_data_ml_times_left_list = []

    item_counter = 1
    big_data_ml_times_data_list.append(0)
    big_data_ml_number_of_distinct_times_data_list.append(0)
    big_data_ml_censored_data_list.append(0)
    big_data_ml_times_left_list.append(len(big_data_ml_sorted_elapsed_time_data_list))

    for item in big_data_ml_sorted_elapsed_time_data_list:
        if item[0] not in big_data_ml_times_data_list :
            if item[1] == 1:
                big_data_ml_times_data_list.append(item[0])
                big_data_ml_number_of_distinct_times_data_list.append(1)
                big_data_ml_censored_data_list.append(0) 
                big_data_ml_times_left_list.append(big_data_ml_times_left_list[item_counter - 1] - (big_data_ml_number_of_distinct_times_data_list[item_counter - 1] + big_data_ml_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                big_data_ml_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                big_data_ml_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                big_data_ml_censored_data_list[item_counter-1]+=1
                
    big_data_ml_survival_time_curve_values = []
    for i in range(len(big_data_ml_times_data_list)):
        if i == 0:
            big_data_ml_survival_time_curve_values.append((big_data_ml_times_left_list[i] - big_data_ml_number_of_distinct_times_data_list[i]) /  big_data_ml_times_left_list[i])
        else:
            big_data_ml_survival_time_curve_values.append(((big_data_ml_times_left_list[i] - big_data_ml_number_of_distinct_times_data_list[i]) /  big_data_ml_times_left_list[i])* big_data_ml_survival_time_curve_values[i-1])
            
    databases_times_data_list = []
    databases_number_of_distinct_times_data_list = []
    databases_censored_data_list = []
    databases_times_left_list = []

    item_counter = 1
    databases_times_data_list.append(0)
    databases_number_of_distinct_times_data_list.append(0)
    databases_censored_data_list.append(0)
    databases_times_left_list.append(len(databases_sorted_elapsed_time_data_list))

    for item in databases_sorted_elapsed_time_data_list:
        if item[0] not in databases_times_data_list :
            if item[1] == 1:
                databases_times_data_list.append(item[0])
                databases_number_of_distinct_times_data_list.append(1)
                databases_censored_data_list.append(0) 
                databases_times_left_list.append(databases_times_left_list[item_counter - 1] - (databases_number_of_distinct_times_data_list[item_counter - 1] + databases_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                databases_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                databases_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                databases_censored_data_list[item_counter-1]+=1
                
    databases_survival_time_curve_values = []
    for i in range(len(databases_times_data_list)):
        if i == 0:
            databases_survival_time_curve_values.append((databases_times_left_list[i] - databases_number_of_distinct_times_data_list[i]) /  databases_times_left_list[i])
        else:
            databases_survival_time_curve_values.append(((databases_times_left_list[i] - databases_number_of_distinct_times_data_list[i]) /  databases_times_left_list[i])* databases_survival_time_curve_values[i-1])
            
    
    platforms_times_data_list = []
    platforms_number_of_distinct_times_data_list = []
    platforms_censored_data_list = []
    platforms_times_left_list = []

    item_counter = 1
    platforms_times_data_list.append(0)
    platforms_number_of_distinct_times_data_list.append(0)
    platforms_censored_data_list.append(0)
    platforms_times_left_list.append(len(platforms_sorted_elapsed_time_data_list))

    for item in platforms_sorted_elapsed_time_data_list:
        if item[0] not in platforms_times_data_list :
            if item[1] == 1:
                platforms_times_data_list.append(item[0])
                platforms_number_of_distinct_times_data_list.append(1)
                platforms_censored_data_list.append(0) 
                platforms_times_left_list.append(platforms_times_left_list[item_counter - 1] - (platforms_number_of_distinct_times_data_list[item_counter - 1] + platforms_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                platforms_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                platforms_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                platforms_censored_data_list[item_counter-1]+=1
                
    platforms_survival_time_curve_values = []
    for i in range(len(platforms_times_data_list)):
        if i == 0:
            platforms_survival_time_curve_values.append((platforms_times_left_list[i] - platforms_number_of_distinct_times_data_list[i]) /  platforms_times_left_list[i])
        else:
            platforms_survival_time_curve_values.append(((platforms_times_left_list[i] - platforms_number_of_distinct_times_data_list[i]) /  platforms_times_left_list[i])* platforms_survival_time_curve_values[i-1])
    
    collaboration_tools_times_data_list = []
    collaboration_tools_number_of_distinct_times_data_list = []
    collaboration_tools_censored_data_list = []
    collaboration_tools_times_left_list = []

    item_counter = 1
    collaboration_tools_times_data_list.append(0)
    collaboration_tools_number_of_distinct_times_data_list.append(0)
    collaboration_tools_censored_data_list.append(0)
    collaboration_tools_times_left_list.append(len(collaboration_tools_sorted_elapsed_time_data_list))

    for item in collaboration_tools_sorted_elapsed_time_data_list:
        if item[0] not in collaboration_tools_times_data_list :
            if item[1] == 1:
                collaboration_tools_times_data_list.append(item[0])
                collaboration_tools_number_of_distinct_times_data_list.append(1)
                collaboration_tools_censored_data_list.append(0) 
                collaboration_tools_times_left_list.append(collaboration_tools_times_left_list[item_counter - 1] - (collaboration_tools_number_of_distinct_times_data_list[item_counter - 1] + collaboration_tools_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                collaboration_tools_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                collaboration_tools_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                collaboration_tools_censored_data_list[item_counter-1]+=1
                
    collaboration_tools_survival_time_curve_values = []
    for i in range(len(collaboration_tools_times_data_list)):
        if i == 0:
            collaboration_tools_survival_time_curve_values.append((collaboration_tools_times_left_list[i] - collaboration_tools_number_of_distinct_times_data_list[i]) /  collaboration_tools_times_left_list[i])
        else:
            collaboration_tools_survival_time_curve_values.append(((collaboration_tools_times_left_list[i] - collaboration_tools_number_of_distinct_times_data_list[i]) /  collaboration_tools_times_left_list[i])* collaboration_tools_survival_time_curve_values[i-1])
        
        
    dev_tools_times_data_list = []
    dev_tools_number_of_distinct_times_data_list = []
    dev_tools_censored_data_list = []
    dev_tools_times_left_list = []

    item_counter = 1
    dev_tools_times_data_list.append(0)
    dev_tools_number_of_distinct_times_data_list.append(0)
    dev_tools_censored_data_list.append(0)
    dev_tools_times_left_list.append(len(dev_tools_sorted_elapsed_time_data_list))

    for item in dev_tools_sorted_elapsed_time_data_list:
        if item[0] not in dev_tools_times_data_list :
            if item[1] == 1:
                dev_tools_times_data_list.append(item[0])
                dev_tools_number_of_distinct_times_data_list.append(1)
                dev_tools_censored_data_list.append(0) 
                dev_tools_times_left_list.append(dev_tools_times_left_list[item_counter - 1] - (dev_tools_number_of_distinct_times_data_list[item_counter - 1] + dev_tools_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                dev_tools_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                dev_tools_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                dev_tools_censored_data_list[item_counter-1]+=1
                
    dev_tools_survival_time_curve_values = []
    for i in range(len(dev_tools_times_data_list)):
        if i == 0:
            dev_tools_survival_time_curve_values.append((dev_tools_times_left_list[i] - dev_tools_number_of_distinct_times_data_list[i]) /  dev_tools_times_left_list[i])
        else:
            dev_tools_survival_time_curve_values.append(((dev_tools_times_left_list[i] - dev_tools_number_of_distinct_times_data_list[i]) /  dev_tools_times_left_list[i])* dev_tools_survival_time_curve_values[i-1])    
        
    
             
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
        sorted(ids_and_votes.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_votes = dict(islice(sorted_ids_and_votes.items(), 10))

    sorted_ids_and_answers = dict(
        sorted(ids_and_answers.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_answers = dict(islice(sorted_ids_and_answers.items(), 10))

    sorted_ids_and_comments = dict(
        sorted(ids_and_comments.items(), reverse=True, key=lambda item: item[1][0]))
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
    top_twenty_tags_and_values_chord = dict(islice(sorted_tags_and_values.items(), 20))  # top 20 for chordDiagram
    top_twenty_tags = list(top_twenty_tags_and_values_chord.keys())  # to 20 tag names for the chord diagram

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
    stacked_deleted_values = [0, 0, 0, 0, 0, 0, 0]  # [languages,frameworks,big data,dbs,platforms,collab tools,dev tools]

    languages_tags_and_values = {}
    frameworks_tags_and_values = {}
    big_data_ml_tags_and_values = {}
    databases_tags_and_values = {}
    platforms_tags_and_values = {}
    collaboration_tools_tags_and_values = {}
    developer_tools_tags_and_values = {}

    for tag in tags:
        if tag in fields_and_techs.keys():
            if tag not in distinct_tags:
                distinct_tags.append(tag)

    for tag in distinct_tags:
        if fields_and_techs.get(tag) == 'Languages':
            radar_values[0] = radar_values[0] + 1
            languages_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Web Frameworks':
            radar_values[1] = radar_values[1] + 1
            frameworks_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Big Data - ML':
            radar_values[2] = radar_values[2] + 1
            big_data_ml_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Databases':
            radar_values[3] = radar_values[3] + 1
            databases_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Platforms':
            radar_values[4] = radar_values[4] + 1
            platforms_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Collaboration Tools':
            radar_values[5] = radar_values[5] + 1
            collaboration_tools_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Developer Tools':
            radar_values[6] = radar_values[6] + 1
            developer_tools_tags_and_values[tag] = tags.count(tag)


    sorted_languages_tags_and_values = dict(
        sorted(languages_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_frameworks_tags_and_values = dict(
        sorted(frameworks_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_big_data_ml_tags_and_values = dict(
        sorted(big_data_ml_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_databases_tags_and_values = dict(
        sorted(databases_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_platforms_tags_and_values = dict(
        sorted(platforms_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_collaboration_tools_tags_and_values = dict(
        sorted(collaboration_tools_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_developer_tools_tags_and_values = dict(
        sorted(developer_tools_tags_and_values.items(), reverse=True, key=lambda item: item[1]))  

    top_10_sorted_languages_tags_and_values = dict(islice(sorted_languages_tags_and_values.items(), 10))
    top_10_sorted_frameworks_tags_and_values = dict(islice(sorted_frameworks_tags_and_values.items(), 10))
    top_10_sorted_big_data_ml_tags_and_values = dict(islice(sorted_big_data_ml_tags_and_values.items(), 10))
    top_10_sorted_databases_tags_and_values = dict(islice(sorted_databases_tags_and_values.items(), 10))
    top_10_sorted_platforms_tags_and_values = dict(islice(sorted_platforms_tags_and_values.items(), 10))
    top_10_sorted_collaboration_tools_tags_and_values = dict(islice(sorted_collaboration_tools_tags_and_values.items(), 10))
    top_10_sorted_developer_tools_tags_and_values = dict(islice(sorted_developer_tools_tags_and_values.items(), 10))

    names_top_10_sorted_languages_tags = list(top_10_sorted_languages_tags_and_values.keys())
    names_top_10_sorted_frameworks_tags = list(top_10_sorted_frameworks_tags_and_values.keys())
    names_top_10_sorted_big_data_ml_tags = list(top_10_sorted_big_data_ml_tags_and_values.keys())
    names_top_10_sorted_databases_tags = list(top_10_sorted_databases_tags_and_values.keys())
    names_top_10_sorted_platforms_tags = list(top_10_sorted_platforms_tags_and_values.keys())
    names_top_10_sorted_collaboration_tools_tags = list(top_10_sorted_collaboration_tools_tags_and_values.keys())
    names_top_10_sorted_developer_tools_tags = list(top_10_sorted_developer_tools_tags_and_values.keys())
    

    for i in range(len(radar_values)):
        radar_values[i] = radar_values[i] / len(distinct_tags)

    # Creation of the stacked bar chart values.
    for question in questions:
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

    # creation of chord diagram matrix
    tag_link_matrix = np.zeros((20, 20)).astype(int)
    tags_to_be_linked = []
    languages_tag_link_matrix = np.zeros((10, 10)).astype(int)
    languages_tags_to_be_linked = []
    frameworks_tag_link_matrix = np.zeros((10, 10)).astype(int)
    frameworks_tags_to_be_linked = []
    big_data_ml_tag_link_matrix = np.zeros((10, 10)).astype(int)
    big_data_ml_tags_to_be_linked = []
    databases_tag_link_matrix = np.zeros((10, 10)).astype(int)
    databases_tags_to_be_linked = []
    platforms_tag_link_matrix = np.zeros((10, 10)).astype(int)
    platforms_tags_to_be_linked = []
    collaborations_tools_tag_link_matrix = np.zeros((10, 10)).astype(int)
    collaborations_tools_tags_to_be_linked = []
    developer_tools_tag_link_matrix = np.zeros((10, 10)).astype(int)
    developer_tools_tags_to_be_linked = []


    for question in questions:
        record_tags = question['tag'].split()
        if [i for i in top_twenty_tags if i in record_tags]:
            for tag in record_tags:
                if tag in top_twenty_tags:
                    tags_to_be_linked.append(top_twenty_tags.index(tag))
            if len(tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        tag_link_matrix[combination[0], combination[1]] += 1
                        tag_link_matrix[combination[1], combination[0]] += 1
            tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_languages_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_languages_tags:
                    languages_tags_to_be_linked.append(names_top_10_sorted_languages_tags.index(tag))
            if len(languages_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(languages_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        languages_tag_link_matrix[combination[0], combination[1]] += 1
                        languages_tag_link_matrix[combination[1], combination[0]] += 1
            languages_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_frameworks_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_frameworks_tags:
                    frameworks_tags_to_be_linked.append(names_top_10_sorted_frameworks_tags.index(tag))
            if len(frameworks_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(frameworks_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        frameworks_tag_link_matrix[combination[0], combination[1]] += 1
                        frameworks_tag_link_matrix[combination[1], combination[0]] += 1
            frameworks_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_big_data_ml_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_big_data_ml_tags:
                    big_data_ml_tags_to_be_linked.append(names_top_10_sorted_big_data_ml_tags.index(tag))
            if len(big_data_ml_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(big_data_ml_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        big_data_ml_tag_link_matrix[combination[0], combination[1]] += 1
                        big_data_ml_tag_link_matrix[combination[1], combination[0]] += 1
            big_data_ml_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_databases_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_databases_tags:
                    databases_tags_to_be_linked.append(names_top_10_sorted_databases_tags.index(tag))
            if len(databases_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(databases_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        databases_tag_link_matrix[combination[0], combination[1]] += 1
                        databases_tag_link_matrix[combination[1], combination[0]] += 1
            databases_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_platforms_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_platforms_tags:
                    platforms_tags_to_be_linked.append(names_top_10_sorted_platforms_tags.index(tag))
            if len(platforms_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(platforms_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        platforms_tag_link_matrix[combination[0], combination[1]] += 1
                        platforms_tag_link_matrix[combination[1], combination[0]] += 1
            platforms_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_collaboration_tools_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_collaboration_tools_tags:
                    collaborations_tools_tags_to_be_linked.append(names_top_10_sorted_collaboration_tools_tags.index(tag))
            if len(collaborations_tools_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(collaborations_tools_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        collaborations_tools_tag_link_matrix[combination[0], combination[1]] += 1
                        collaborations_tools_tag_link_matrix[combination[1], combination[0]] += 1
            collaborations_tools_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_developer_tools_tags if i in record_tags]:    
            for tag in record_tags:
                if tag in names_top_10_sorted_developer_tools_tags:
                    developer_tools_tags_to_be_linked.append(names_top_10_sorted_developer_tools_tags.index(tag))
            if len(developer_tools_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(developer_tools_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        developer_tools_tag_link_matrix[combination[0], combination[1]] += 1
                        developer_tools_tag_link_matrix[combination[1], combination[0]] += 1
            developer_tools_tags_to_be_linked.clear()

    list_tag_link_matrix = np.array2string(tag_link_matrix, separator=",")
    list_languages_tag_link_matrix = np.array2string(languages_tag_link_matrix, separator=",")
    list_frameworks_tag_link_matrix = np.array2string(frameworks_tag_link_matrix, separator=",")
    list_big_data_ml_tag_link_matrix = np.array2string(big_data_ml_tag_link_matrix, separator=",")
    list_databases_tag_link_matrix = np.array2string(databases_tag_link_matrix, separator=",")
    list_platforms_tag_link_matrix = np.array2string(platforms_tag_link_matrix, separator=",")
    list_collaboration_tools_tag_link_matrix = np.array2string(collaborations_tools_tag_link_matrix, separator=",")
    list_developer_tools_tag_link_matrix = np.array2string(developer_tools_tag_link_matrix, separator=",")

    return render_template('index.html', questions=questions, question_count=question_count, users=users, labels=labels,
                           values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues, latLngInt=latLngInt, latitudes=latitudes,
                           longitudes=longitudes,
                           distinct_technologies=distinct_technologies,
                           stacked_open_values=stacked_open_values, stacked_closed_values=stacked_closed_values,
                           stacked_deleted_values=stacked_deleted_values,
                           radar_values=radar_values, added_values=added_values, avgNumberOfAnswers=avgNumberOfAnswers,
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
                           top_10_dev_tools_comments=top_10_dev_tools_comments,
                           date_from=date_from, date_to=date_to, 
                           list_tag_link_matrix=list_tag_link_matrix, top_twenty_tags=top_twenty_tags, 
                           list_languages_tag_link_matrix = list_languages_tag_link_matrix, names_top_10_sorted_languages_tags = names_top_10_sorted_languages_tags,
                           list_frameworks_tag_link_matrix = list_frameworks_tag_link_matrix, names_top_10_sorted_frameworks_tags = names_top_10_sorted_frameworks_tags,
                           list_big_data_ml_tag_link_matrix = list_big_data_ml_tag_link_matrix, names_top_10_sorted_big_data_ml_tags = names_top_10_sorted_big_data_ml_tags,
                           list_databases_tag_link_matrix = list_databases_tag_link_matrix, names_top_10_sorted_databases_tags = names_top_10_sorted_databases_tags,
                           list_platforms_tag_link_matrix = list_platforms_tag_link_matrix, names_top_10_sorted_platforms_tags = names_top_10_sorted_platforms_tags,
                           list_collaboration_tools_tag_link_matrix = list_collaboration_tools_tag_link_matrix, names_top_10_sorted_collaboration_tools_tags = names_top_10_sorted_collaboration_tools_tags,
                           list_developer_tools_tag_link_matrix = list_developer_tools_tag_link_matrix, names_top_10_sorted_developer_tools_tags = names_top_10_sorted_developer_tools_tags,
                           times_data_list = times_data_list, survival_time_curve_values = survival_time_curve_values, 
                           languages_times_data_list = languages_times_data_list, languages_survival_time_curve_values = languages_survival_time_curve_values,
                           web_frameworks_times_data_list = web_frameworks_times_data_list, web_frameworks_survival_time_curve_values = web_frameworks_survival_time_curve_values,
                           big_data_ml_times_data_list = big_data_ml_times_data_list, big_data_ml_survival_time_curve_values = big_data_ml_survival_time_curve_values,
                           databases_times_data_list = databases_times_data_list, databases_survival_time_curve_values = databases_survival_time_curve_values,
                           platforms_times_data_list = platforms_times_data_list, platforms_survival_time_curve_values = platforms_survival_time_curve_values,
                           collaboration_tools_times_data_list = collaboration_tools_times_data_list, collaboration_tools_survival_time_curve_values = collaboration_tools_survival_time_curve_values,
                           dev_tools_times_data_list = dev_tools_times_data_list, dev_tools_survival_time_curve_values = dev_tools_survival_time_curve_values
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
    if closed == 1: # all questions
        query = {'timestamps': {'$gte': date_from, '$lte': date_to}}
    elif closed == 0: # only open questions
        query = {
            "$and": [
                {"timestamps": {"$gte": date_from, "$lte": date_to}},
                {"$and": [
                    {"closed": closed},
                    {"deleted": closed}
                ]}
            ]
        }

    questions = covidCollection.find(query)  #load questions from collection

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
    elapsed_time_data_list = []
    languages_elapsed_time_data_list = []
    web_frameworks_elapsed_time_data_list = []
    big_data_ml_elapsed_time_data_list = []
    databases_elapsed_time_data_list = []
    platforms_elapsed_time_data_list = []
    collaboration_tools_elapsed_time_data_list = []
    dev_tools_elapsed_time_data_list = []

    fields_and_techs = {}
    for technology in technologies:
        fields_and_techs.update({technology['field'].lower(): technology['technology']})

    question_count = 0
    for question in questions:
        question_count += 1
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
        
        question_time = datetime.fromisoformat(question['timestamps'][:-1]).replace(tzinfo=timezone.utc)
        if question_time:           
            if question['first_answer'] != 'No answers':
                first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                event = 1   
            else:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                event = 0    
            if hour_diff!=0.0:
                elapsed_time_data_list.append([hour_diff,event])
        #########################
        for q_tag in dif_tags:
            if fields_and_techs.get(q_tag) == 'Languages':
                languages.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        languages_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Web Frameworks':
                web_frameworks.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        web_frameworks_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Big Data - ML':
                big_data_ml.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        big_data_ml_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Databases':
                databases.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        databases_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Platforms':
                platforms.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        platforms_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Collaboration Tools':
                collaboration_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        collaboration_tools_elapsed_time_data_list.append([hour_diff,event])
            if fields_and_techs.get(q_tag) == 'Developer Tools':
                dev_tools.update({q_link: [int(question['votes']), int(question['answers']), int(question['comments']), question['question_title']]})
                if question_time:           
                    if question['first_answer'] != 'No answers':
                        first_answer_time = datetime.fromisoformat(question['first_answer'][:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((first_answer_time - question_time).total_seconds() / 3600,1)
                        event = 1   
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"Z"
                        current_time_formatted = datetime.fromisoformat(current_time[:-1]).replace(tzinfo=timezone.utc)
                        hour_diff = round((current_time_formatted - question_time).total_seconds() / 3600,1)
                        event = 0    
                    if hour_diff!=0.0:
                        dev_tools_elapsed_time_data_list.append([hour_diff,event])
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
    
    sorted_elapsed_time_data_list = sorted(elapsed_time_data_list, key=itemgetter(0))
    languages_sorted_elapsed_time_data_list = sorted(languages_elapsed_time_data_list, key=itemgetter(0))
    web_frameworks_sorted_elapsed_time_data_list = sorted(web_frameworks_elapsed_time_data_list, key=itemgetter(0))
    big_data_ml_sorted_elapsed_time_data_list = sorted(big_data_ml_elapsed_time_data_list, key=itemgetter(0))
    databases_sorted_elapsed_time_data_list = sorted(databases_elapsed_time_data_list, key=itemgetter(0))
    platforms_sorted_elapsed_time_data_list = sorted(platforms_elapsed_time_data_list, key=itemgetter(0))
    collaboration_tools_sorted_elapsed_time_data_list = sorted(collaboration_tools_elapsed_time_data_list, key=itemgetter(0))
    dev_tools_sorted_elapsed_time_data_list = sorted(dev_tools_elapsed_time_data_list, key=itemgetter(0))
    
    
    times_data_list = []
    number_of_distinct_times_data_list = []
    censored_data_list = []
    times_left_list = []
    
    item_counter = 1
    times_data_list.append(0)
    number_of_distinct_times_data_list.append(0)
    censored_data_list.append(0)
    times_left_list.append(len(sorted_elapsed_time_data_list))
    
    for item in sorted_elapsed_time_data_list:
        if item[0] not in times_data_list :
            if item[1] == 1:
                times_data_list.append(item[0])
                number_of_distinct_times_data_list.append(1)
                censored_data_list.append(0) 
                times_left_list.append(times_left_list[item_counter - 1] - (number_of_distinct_times_data_list[item_counter - 1] + censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                censored_data_list[item_counter-1]+=1
        
    survival_time_curve_values = []
    for i in range(len(times_data_list)):
        if i == 0:
            survival_time_curve_values.append((times_left_list[i] - number_of_distinct_times_data_list[i]) /  times_left_list[i])
        else:
            survival_time_curve_values.append(((times_left_list[i] - number_of_distinct_times_data_list[i]) /  times_left_list[i])* survival_time_curve_values[i-1])
    
    
    
    languages_times_data_list = []
    languages_number_of_distinct_times_data_list = []
    languages_censored_data_list = []
    languages_times_left_list = []

    item_counter = 1
    languages_times_data_list.append(0)
    languages_number_of_distinct_times_data_list.append(0)
    languages_censored_data_list.append(0)
    languages_times_left_list.append(len(languages_sorted_elapsed_time_data_list))

    for item in languages_sorted_elapsed_time_data_list:
        if item[0] not in languages_times_data_list :
            if item[1] == 1:
                languages_times_data_list.append(item[0])
                languages_number_of_distinct_times_data_list.append(1)
                languages_censored_data_list.append(0) 
                languages_times_left_list.append(languages_times_left_list[item_counter - 1] - (languages_number_of_distinct_times_data_list[item_counter - 1] + languages_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                languages_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                languages_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                languages_censored_data_list[item_counter-1]+=1

    languages_survival_time_curve_values = []
    for i in range(len(languages_times_data_list)):
        if i == 0:
            languages_survival_time_curve_values.append((languages_times_left_list[i] - languages_number_of_distinct_times_data_list[i]) /  languages_times_left_list[i])
        else:
            languages_survival_time_curve_values.append(((languages_times_left_list[i] - languages_number_of_distinct_times_data_list[i]) /  languages_times_left_list[i]) * languages_survival_time_curve_values[i-1])
        
    
    
    web_frameworks_times_data_list = []
    web_frameworks_number_of_distinct_times_data_list = []
    web_frameworks_censored_data_list = []
    web_frameworks_times_left_list = []

    item_counter = 1
    web_frameworks_times_data_list.append(0)
    web_frameworks_number_of_distinct_times_data_list.append(0)
    web_frameworks_censored_data_list.append(0)
    web_frameworks_times_left_list.append(len(web_frameworks_sorted_elapsed_time_data_list))

    for item in web_frameworks_sorted_elapsed_time_data_list:
        if item[0] not in web_frameworks_times_data_list :
            if item[1] == 1:
                web_frameworks_times_data_list.append(item[0])
                web_frameworks_number_of_distinct_times_data_list.append(1)
                web_frameworks_censored_data_list.append(0) 
                web_frameworks_times_left_list.append(web_frameworks_times_left_list[item_counter - 1] - (web_frameworks_number_of_distinct_times_data_list[item_counter - 1] + web_frameworks_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                web_frameworks_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                web_frameworks_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                web_frameworks_censored_data_list[item_counter-1]+=1
                
    web_frameworks_survival_time_curve_values = []
    for i in range(len(web_frameworks_times_data_list)):
        if i == 0:
            web_frameworks_survival_time_curve_values.append((web_frameworks_times_left_list[i] - web_frameworks_number_of_distinct_times_data_list[i]) /  web_frameworks_times_left_list[i])
        else:
            web_frameworks_survival_time_curve_values.append(((web_frameworks_times_left_list[i] - web_frameworks_number_of_distinct_times_data_list[i]) /  web_frameworks_times_left_list[i])* web_frameworks_survival_time_curve_values[i-1])
        
        

    big_data_ml_times_data_list = []
    big_data_ml_number_of_distinct_times_data_list = []
    big_data_ml_censored_data_list = []
    big_data_ml_times_left_list = []

    item_counter = 1
    big_data_ml_times_data_list.append(0)
    big_data_ml_number_of_distinct_times_data_list.append(0)
    big_data_ml_censored_data_list.append(0)
    big_data_ml_times_left_list.append(len(big_data_ml_sorted_elapsed_time_data_list))

    for item in big_data_ml_sorted_elapsed_time_data_list:
        if item[0] not in big_data_ml_times_data_list :
            if item[1] == 1:
                big_data_ml_times_data_list.append(item[0])
                big_data_ml_number_of_distinct_times_data_list.append(1)
                big_data_ml_censored_data_list.append(0) 
                big_data_ml_times_left_list.append(big_data_ml_times_left_list[item_counter - 1] - (big_data_ml_number_of_distinct_times_data_list[item_counter - 1] + big_data_ml_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                big_data_ml_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                big_data_ml_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                big_data_ml_censored_data_list[item_counter-1]+=1
                
    big_data_ml_survival_time_curve_values = []
    for i in range(len(big_data_ml_times_data_list)):
        if i == 0:
            big_data_ml_survival_time_curve_values.append((big_data_ml_times_left_list[i] - big_data_ml_number_of_distinct_times_data_list[i]) /  big_data_ml_times_left_list[i])
        else:
            big_data_ml_survival_time_curve_values.append(((big_data_ml_times_left_list[i] - big_data_ml_number_of_distinct_times_data_list[i]) /  big_data_ml_times_left_list[i])* big_data_ml_survival_time_curve_values[i-1])
            
    databases_times_data_list = []
    databases_number_of_distinct_times_data_list = []
    databases_censored_data_list = []
    databases_times_left_list = []

    item_counter = 1
    databases_times_data_list.append(0)
    databases_number_of_distinct_times_data_list.append(0)
    databases_censored_data_list.append(0)
    databases_times_left_list.append(len(databases_sorted_elapsed_time_data_list))

    for item in databases_sorted_elapsed_time_data_list:
        if item[0] not in databases_times_data_list :
            if item[1] == 1:
                databases_times_data_list.append(item[0])
                databases_number_of_distinct_times_data_list.append(1)
                databases_censored_data_list.append(0) 
                databases_times_left_list.append(databases_times_left_list[item_counter - 1] - (databases_number_of_distinct_times_data_list[item_counter - 1] + databases_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                databases_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                databases_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                databases_censored_data_list[item_counter-1]+=1
                
    databases_survival_time_curve_values = []
    for i in range(len(databases_times_data_list)):
        if i == 0:
            databases_survival_time_curve_values.append((databases_times_left_list[i] - databases_number_of_distinct_times_data_list[i]) /  databases_times_left_list[i])
        else:
            databases_survival_time_curve_values.append(((databases_times_left_list[i] - databases_number_of_distinct_times_data_list[i]) /  databases_times_left_list[i])* databases_survival_time_curve_values[i-1])
            
    
    platforms_times_data_list = []
    platforms_number_of_distinct_times_data_list = []
    platforms_censored_data_list = []
    platforms_times_left_list = []

    item_counter = 1
    platforms_times_data_list.append(0)
    platforms_number_of_distinct_times_data_list.append(0)
    platforms_censored_data_list.append(0)
    platforms_times_left_list.append(len(platforms_sorted_elapsed_time_data_list))

    for item in platforms_sorted_elapsed_time_data_list:
        if item[0] not in platforms_times_data_list :
            if item[1] == 1:
                platforms_times_data_list.append(item[0])
                platforms_number_of_distinct_times_data_list.append(1)
                platforms_censored_data_list.append(0) 
                platforms_times_left_list.append(platforms_times_left_list[item_counter - 1] - (platforms_number_of_distinct_times_data_list[item_counter - 1] + platforms_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                platforms_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                platforms_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                platforms_censored_data_list[item_counter-1]+=1
                
    platforms_survival_time_curve_values = []
    for i in range(len(platforms_times_data_list)):
        if i == 0:
            platforms_survival_time_curve_values.append((platforms_times_left_list[i] - platforms_number_of_distinct_times_data_list[i]) /  platforms_times_left_list[i])
        else:
            platforms_survival_time_curve_values.append(((platforms_times_left_list[i] - platforms_number_of_distinct_times_data_list[i]) /  platforms_times_left_list[i])* platforms_survival_time_curve_values[i-1])
    
    
    
    collaboration_tools_times_data_list = []
    collaboration_tools_number_of_distinct_times_data_list = []
    collaboration_tools_censored_data_list = []
    collaboration_tools_times_left_list = []

    item_counter = 1
    collaboration_tools_times_data_list.append(0)
    collaboration_tools_number_of_distinct_times_data_list.append(0)
    collaboration_tools_censored_data_list.append(0)
    collaboration_tools_times_left_list.append(len(collaboration_tools_sorted_elapsed_time_data_list))

    for item in collaboration_tools_sorted_elapsed_time_data_list:
        if item[0] not in collaboration_tools_times_data_list :
            if item[1] == 1:
                collaboration_tools_times_data_list.append(item[0])
                collaboration_tools_number_of_distinct_times_data_list.append(1)
                collaboration_tools_censored_data_list.append(0) 
                collaboration_tools_times_left_list.append(collaboration_tools_times_left_list[item_counter - 1] - (collaboration_tools_number_of_distinct_times_data_list[item_counter - 1] + collaboration_tools_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                collaboration_tools_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                collaboration_tools_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                collaboration_tools_censored_data_list[item_counter-1]+=1
                
    collaboration_tools_survival_time_curve_values = []
    for i in range(len(collaboration_tools_times_data_list)):
        if i == 0:
            collaboration_tools_survival_time_curve_values.append((collaboration_tools_times_left_list[i] - collaboration_tools_number_of_distinct_times_data_list[i]) /  collaboration_tools_times_left_list[i])
        else:
            collaboration_tools_survival_time_curve_values.append(((collaboration_tools_times_left_list[i] - collaboration_tools_number_of_distinct_times_data_list[i]) /  collaboration_tools_times_left_list[i])* collaboration_tools_survival_time_curve_values[i-1])
        
        
    
    dev_tools_times_data_list = []
    dev_tools_number_of_distinct_times_data_list = []
    dev_tools_censored_data_list = []
    dev_tools_times_left_list = []

    item_counter = 1
    dev_tools_times_data_list.append(0)
    dev_tools_number_of_distinct_times_data_list.append(0)
    dev_tools_censored_data_list.append(0)
    dev_tools_times_left_list.append(len(dev_tools_sorted_elapsed_time_data_list))

    for item in dev_tools_sorted_elapsed_time_data_list:
        if item[0] not in dev_tools_times_data_list :
            if item[1] == 1:
                dev_tools_times_data_list.append(item[0])
                dev_tools_number_of_distinct_times_data_list.append(1)
                dev_tools_censored_data_list.append(0) 
                dev_tools_times_left_list.append(dev_tools_times_left_list[item_counter - 1] - (dev_tools_number_of_distinct_times_data_list[item_counter - 1] + dev_tools_censored_data_list[item_counter-1]))  
                item_counter+=1        
            else:
                dev_tools_censored_data_list[item_counter-1]+=1
            
        else:         
            if item[1] == 1:
                dev_tools_number_of_distinct_times_data_list[item_counter - 1]+=1
            else:
                dev_tools_censored_data_list[item_counter-1]+=1
                
    dev_tools_survival_time_curve_values = []
    for i in range(len(dev_tools_times_data_list)):
        if i == 0:
            dev_tools_survival_time_curve_values.append((dev_tools_times_left_list[i] - dev_tools_number_of_distinct_times_data_list[i]) /  dev_tools_times_left_list[i])
        else:
            dev_tools_survival_time_curve_values.append(((dev_tools_times_left_list[i] - dev_tools_number_of_distinct_times_data_list[i]) /  dev_tools_times_left_list[i])* dev_tools_survival_time_curve_values[i-1])    
        
    
             
    distinct_locations = Counter(locations)
    for key, value in distinct_locations.items():
        location_name.append(key)
        location_question.append(value)

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
        sorted(ids_and_votes.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_votes = dict(islice(sorted_ids_and_votes.items(), 10))

    sorted_ids_and_answers = dict(
        sorted(ids_and_answers.items(), reverse=True, key=lambda item: item[1][0]))
    top_10_sorted_ids_and_answers = dict(islice(sorted_ids_and_answers.items(), 10))

    sorted_ids_and_comments = dict(
        sorted(ids_and_comments.items(), reverse=True, key=lambda item: item[1][0]))
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
    top_twenty_tags_and_values_chord = dict(islice(sorted_tags_and_values.items(), 20))  # top 20 for chordDiagram
    top_twenty_tags = list(top_twenty_tags_and_values_chord.keys())  # to 10 tag names for the chord diagram

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
    stacked_deleted_values = [0, 0, 0, 0, 0, 0, 0]  # [languages,frameworks,big data,dbs,platforms,collab tools,dev tools]

    languages_tags_and_values = {}
    frameworks_tags_and_values = {}
    big_data_ml_tags_and_values = {}
    databases_tags_and_values = {}
    platforms_tags_and_values = {}
    collaboration_tools_tags_and_values = {}
    developer_tools_tags_and_values = {}

    for tag in tags:
        if tag in fields_and_techs.keys():
            if tag not in distinct_tags:
                distinct_tags.append(tag)

    for tag in distinct_tags:
        if fields_and_techs.get(tag) == 'Languages':
            radar_values[0] = radar_values[0] + 1
            languages_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Web Frameworks':
            radar_values[1] = radar_values[1] + 1
            frameworks_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Big Data - ML':
            radar_values[2] = radar_values[2] + 1
            big_data_ml_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Databases':
            radar_values[3] = radar_values[3] + 1
            databases_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Platforms':
            radar_values[4] = radar_values[4] + 1
            platforms_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Collaboration Tools':
            radar_values[5] = radar_values[5] + 1
            collaboration_tools_tags_and_values[tag] = tags.count(tag)
        elif fields_and_techs.get(tag) == 'Developer Tools':
            radar_values[6] = radar_values[6] + 1
            developer_tools_tags_and_values[tag] = tags.count(tag)


    sorted_languages_tags_and_values = dict(
        sorted(languages_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_frameworks_tags_and_values = dict(
        sorted(frameworks_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_big_data_ml_tags_and_values = dict(
        sorted(big_data_ml_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_databases_tags_and_values = dict(
        sorted(databases_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_platforms_tags_and_values = dict(
        sorted(platforms_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_collaboration_tools_tags_and_values = dict(
        sorted(collaboration_tools_tags_and_values.items(), reverse=True, key=lambda item: item[1]))
    sorted_developer_tools_tags_and_values = dict(
        sorted(developer_tools_tags_and_values.items(), reverse=True, key=lambda item: item[1]))  

    top_10_sorted_languages_tags_and_values = dict(islice(sorted_languages_tags_and_values.items(), 10))
    top_10_sorted_frameworks_tags_and_values = dict(islice(sorted_frameworks_tags_and_values.items(), 10))
    top_10_sorted_big_data_ml_tags_and_values = dict(islice(sorted_big_data_ml_tags_and_values.items(), 10))
    top_10_sorted_databases_tags_and_values = dict(islice(sorted_databases_tags_and_values.items(), 10))
    top_10_sorted_platforms_tags_and_values = dict(islice(sorted_platforms_tags_and_values.items(), 10))
    top_10_sorted_collaboration_tools_tags_and_values = dict(islice(sorted_collaboration_tools_tags_and_values.items(), 10))
    top_10_sorted_developer_tools_tags_and_values = dict(islice(sorted_developer_tools_tags_and_values.items(), 10))

    names_top_10_sorted_languages_tags = list(top_10_sorted_languages_tags_and_values.keys())
    names_top_10_sorted_frameworks_tags = list(top_10_sorted_frameworks_tags_and_values.keys())
    names_top_10_sorted_big_data_ml_tags = list(top_10_sorted_big_data_ml_tags_and_values.keys())
    names_top_10_sorted_databases_tags = list(top_10_sorted_databases_tags_and_values.keys())
    names_top_10_sorted_platforms_tags = list(top_10_sorted_platforms_tags_and_values.keys())
    names_top_10_sorted_collaboration_tools_tags = list(top_10_sorted_collaboration_tools_tags_and_values.keys())
    names_top_10_sorted_developer_tools_tags = list(top_10_sorted_developer_tools_tags_and_values.keys())
    

    for i in range(len(radar_values)):
        radar_values[i] = radar_values[i] / len(distinct_tags)

    # Creation of the stacked bar chart values.
    for question in questions:
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

    # creation of chord diagram matrix
    tag_link_matrix = np.zeros((20, 20)).astype(int)
    tags_to_be_linked = []
    languages_tag_link_matrix = np.zeros((10, 10)).astype(int)
    languages_tags_to_be_linked = []
    frameworks_tag_link_matrix = np.zeros((10, 10)).astype(int)
    frameworks_tags_to_be_linked = []
    big_data_ml_tag_link_matrix = np.zeros((10, 10)).astype(int)
    big_data_ml_tags_to_be_linked = []
    databases_tag_link_matrix = np.zeros((10, 10)).astype(int)
    databases_tags_to_be_linked = []
    platforms_tag_link_matrix = np.zeros((10, 10)).astype(int)
    platforms_tags_to_be_linked = []
    collaborations_tools_tag_link_matrix = np.zeros((10, 10)).astype(int)
    collaborations_tools_tags_to_be_linked = []
    developer_tools_tag_link_matrix = np.zeros((10, 10)).astype(int)
    developer_tools_tags_to_be_linked = []


    for question in questions:
        record_tags = question['tag'].split()
        if [i for i in top_twenty_tags if i in record_tags]:
            for tag in record_tags:
                if tag in top_twenty_tags:
                    tags_to_be_linked.append(top_twenty_tags.index(tag))
            if len(tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        tag_link_matrix[combination[0], combination[1]] += 1
                        tag_link_matrix[combination[1], combination[0]] += 1
            tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_languages_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_languages_tags:
                    languages_tags_to_be_linked.append(names_top_10_sorted_languages_tags.index(tag))
            if len(languages_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(languages_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        languages_tag_link_matrix[combination[0], combination[1]] += 1
                        languages_tag_link_matrix[combination[1], combination[0]] += 1
            languages_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_frameworks_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_frameworks_tags:
                    frameworks_tags_to_be_linked.append(names_top_10_sorted_frameworks_tags.index(tag))
            if len(frameworks_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(frameworks_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        frameworks_tag_link_matrix[combination[0], combination[1]] += 1
                        frameworks_tag_link_matrix[combination[1], combination[0]] += 1
            frameworks_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_big_data_ml_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_big_data_ml_tags:
                    big_data_ml_tags_to_be_linked.append(names_top_10_sorted_big_data_ml_tags.index(tag))
            if len(big_data_ml_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(big_data_ml_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        big_data_ml_tag_link_matrix[combination[0], combination[1]] += 1
                        big_data_ml_tag_link_matrix[combination[1], combination[0]] += 1
            big_data_ml_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_databases_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_databases_tags:
                    databases_tags_to_be_linked.append(names_top_10_sorted_databases_tags.index(tag))
            if len(databases_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(databases_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        databases_tag_link_matrix[combination[0], combination[1]] += 1
                        databases_tag_link_matrix[combination[1], combination[0]] += 1
            databases_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_platforms_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_platforms_tags:
                    platforms_tags_to_be_linked.append(names_top_10_sorted_platforms_tags.index(tag))
            if len(platforms_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(platforms_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        platforms_tag_link_matrix[combination[0], combination[1]] += 1
                        platforms_tag_link_matrix[combination[1], combination[0]] += 1
            platforms_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_collaboration_tools_tags if i in record_tags]:
            for tag in record_tags:
                if tag in names_top_10_sorted_collaboration_tools_tags:
                    collaborations_tools_tags_to_be_linked.append(names_top_10_sorted_collaboration_tools_tags.index(tag))
            if len(collaborations_tools_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(collaborations_tools_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        collaborations_tools_tag_link_matrix[combination[0], combination[1]] += 1
                        collaborations_tools_tag_link_matrix[combination[1], combination[0]] += 1
            collaborations_tools_tags_to_be_linked.clear()
        if [i for i in names_top_10_sorted_developer_tools_tags if i in record_tags]:    
            for tag in record_tags:
                if tag in names_top_10_sorted_developer_tools_tags:
                    developer_tools_tags_to_be_linked.append(names_top_10_sorted_developer_tools_tags.index(tag))
            if len(developer_tools_tags_to_be_linked) > 1:
                combinations_of_tags = list(combinations(developer_tools_tags_to_be_linked, 2))
                for combination in combinations_of_tags:
                    if combination[0] != combination[1]:
                        developer_tools_tag_link_matrix[combination[0], combination[1]] += 1
                        developer_tools_tag_link_matrix[combination[1], combination[0]] += 1
            developer_tools_tags_to_be_linked.clear()

    # print(not np.any(developer_tools_tag_link_matrix))
    list_tag_link_matrix = np.array2string(tag_link_matrix, separator=",")
    list_languages_tag_link_matrix = np.array2string(languages_tag_link_matrix, separator=",")
    list_frameworks_tag_link_matrix = np.array2string(frameworks_tag_link_matrix, separator=",")
    list_big_data_ml_tag_link_matrix = np.array2string(big_data_ml_tag_link_matrix, separator=",")
    list_databases_tag_link_matrix = np.array2string(databases_tag_link_matrix, separator=",")
    list_platforms_tag_link_matrix = np.array2string(platforms_tag_link_matrix, separator=",")
    list_collaboration_tools_tag_link_matrix = np.array2string(collaborations_tools_tag_link_matrix, separator=",")
    list_developer_tools_tag_link_matrix = np.array2string(developer_tools_tag_link_matrix, separator=",")
    

    return render_template('index.html', questions=questions, question_count=question_count, users=users, labels=labels,
                           values=values,
                           list_of_tags_and_values=list_of_tags_and_values, barChartLabels=barChartLabels,
                           barChartValues=barChartValues, latLngInt=latLngInt, latitudes=latitudes,
                           longitudes=longitudes,
                           distinct_technologies=distinct_technologies,
                           stacked_open_values=stacked_open_values, stacked_closed_values=stacked_closed_values,
                           stacked_deleted_values=stacked_deleted_values,
                           radar_values=radar_values, added_values=added_values, avgNumberOfAnswers=avgNumberOfAnswers,
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
                           top_10_dev_tools_comments=top_10_dev_tools_comments,
                           date_from=date_from, date_to=date_to, 
                           list_tag_link_matrix=list_tag_link_matrix, top_twenty_tags=top_twenty_tags, 
                           list_languages_tag_link_matrix = list_languages_tag_link_matrix, names_top_10_sorted_languages_tags = names_top_10_sorted_languages_tags,
                           list_frameworks_tag_link_matrix = list_frameworks_tag_link_matrix, names_top_10_sorted_frameworks_tags = names_top_10_sorted_frameworks_tags,
                           list_big_data_ml_tag_link_matrix = list_big_data_ml_tag_link_matrix, names_top_10_sorted_big_data_ml_tags = names_top_10_sorted_big_data_ml_tags,
                           list_databases_tag_link_matrix = list_databases_tag_link_matrix, names_top_10_sorted_databases_tags = names_top_10_sorted_databases_tags,
                           list_platforms_tag_link_matrix = list_platforms_tag_link_matrix, names_top_10_sorted_platforms_tags = names_top_10_sorted_platforms_tags,
                           list_collaboration_tools_tag_link_matrix = list_collaboration_tools_tag_link_matrix, names_top_10_sorted_collaboration_tools_tags = names_top_10_sorted_collaboration_tools_tags,
                           list_developer_tools_tag_link_matrix = list_developer_tools_tag_link_matrix, names_top_10_sorted_developer_tools_tags = names_top_10_sorted_developer_tools_tags,
                           times_data_list = times_data_list, survival_time_curve_values = survival_time_curve_values, 
                           languages_times_data_list = languages_times_data_list, languages_survival_time_curve_values = languages_survival_time_curve_values,
                           web_frameworks_times_data_list = web_frameworks_times_data_list, web_frameworks_survival_time_curve_values = web_frameworks_survival_time_curve_values,
                           big_data_ml_times_data_list = big_data_ml_times_data_list, big_data_ml_survival_time_curve_values = big_data_ml_survival_time_curve_values,
                           databases_times_data_list = databases_times_data_list, databases_survival_time_curve_values = databases_survival_time_curve_values,
                           platforms_times_data_list = platforms_times_data_list, platforms_survival_time_curve_values = platforms_survival_time_curve_values,
                           collaboration_tools_times_data_list = collaboration_tools_times_data_list, collaboration_tools_survival_time_curve_values = collaboration_tools_survival_time_curve_values,
                           dev_tools_times_data_list = dev_tools_times_data_list, dev_tools_survival_time_curve_values = dev_tools_survival_time_curve_values
                           )
