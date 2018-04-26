from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from flask import jsonify, request
from werkzeug.exceptions import abort

from app.model.Question import Question
from app.model.Area import Area
from app.model.Group import Group
from app.model.Station import Station
from app.model.Option import Option
from app.model.Answer import Answer

from app.api import bp

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

    if ((not request.json) or (not "statement" in request.json) or (not "option_type" in request.json) or (
    not "area" in request.json) or (not "group" in request.json)):
        abort(400)

    statement = value["statement"]
    option_type = value["option_type"]
    area = value["area"]
    group = value["group"]

    if (ifQuestion(area, group) == False):
        abort(404)

    question = Question(statement, option_type, group, area)

    return question

def outJsonQuestion(question):
    myjson = jsonify({
        "$uri": "/question/" + str(question.id_question),
        "statement": question.statement,
        "option_type": question.option_type,
        "area": {
            "$ref": "/area/" + str(question.id_area)
        },
        "group": {
            "$ref": "/group/" + str(question.id_group)
        }
    })

    return myjson


@bp.route('/question', methods=['POST'])
def postQuestion():
    inJsonQuestion().post_question()
    question = Question().get_last_ques()

    return outJsonQuestion(question)


@bp.route('/question/<int:id>', methods=['PATCH'])
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
