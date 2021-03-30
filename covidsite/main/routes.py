from flask import Blueprint, render_template

from covidsite.extensions import mongo

main = Blueprint('main', __name__)


@main.route('/')
def index():
    covidcollection = mongo.db.questions
    questions = covidcollection.find().count()

    return render_template('index.html', questions=questions)
