from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from flask import jsonify, request
from werkzeug.exceptions import abort

from model.Question import Question
from model.Area import Area
from model.Group import Group
from model.Station import Station
from model.Option import Option
from model import app
from model.Answer import Answer


class QuestionResource(ModelResource):
    options = Relation('option')

    class Meta:
        model = Question

    class Schema:
        group = fields.ToOne('group')
        area = fields.ToOne('area')


def ifQuestion(area, group):
    areaAux = Area().get_area(area)
    if (areaAux):
        groupAux = Group().get_group(group)
        if (groupAux):
            stationAux = Station().get_station(groupAux.id_station)
            if (stationAux):
                if (areaAux.id_ecoe == stationAux.id_ecoe):
                    return True
    return False


def inJsonQuestion():
    value = request.json

    if ((not request.json) or (not "wording" in request.json) or (not "option_type" in request.json) or (
    not "area" in request.json) or (not "group" in request.json)):
        abort(400)

    wording = value["wording"]
    option_type = value["option_type"]
    area = value["area"]
    group = value["group"]

    if (ifQuestion(area, group) == False):
        abort(404)

    question = Question(wording, option_type, group, area)

    return question


def outJsonQuestion(question):
    myjson = jsonify({
        "$uri": "/question/" + str(question.id_question),
        "wording": question.wording,
        "option_type": question.option_type,
        "area": {
            "$ref": "/area/" + str(question.id_area)
        },
        "group": {
            "$ref": "/group/" + str(question.id_group)
        }
    })

    return myjson


@app.route('/question', methods=['POST'])
def postQuestion():
    inJsonQuestion().post_question()
    question = Question().get_last_ques()

    return outJsonQuestion(question)


@app.route('/question/<int:id>', methods=['PATCH'])
def pathQuestion(id):
    questionOld = Question().get_question(id)

    if (questionOld):
        questionOld.path_question(inJsonQuestion())
        return outJsonQuestion(questionOld)
    else:
        abort(404)


class OptionResource(ModelResource):
    class Meta:
        model = Option

    class Schema:
        question = fields.ToOne('question')


class AnswerResource(ModelResource):
    class Meta:
        model = Answer

    class Schema:
        student = fields.ToOne('student')
        option = fields.ToOne('option')
