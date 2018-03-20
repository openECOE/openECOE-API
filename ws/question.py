from flask_potion import ModelResource, fields, manager
from flask_potion.routes import Relation, Route, FieldSet

from flask import jsonify, request
from werkzeug.exceptions import abort

from model.Question import Question
from model.Area import Area
from model.Group import Group
from model.Station import Station

from model import app

class QuestionResource(ModelResource):
    options = Relation('opt')

    class Meta:
        model = Question

    class Schema:
        group = fields.ToOne('group')
        area = fields.ToOne('area')

@app.route('/ques', methods=['POST'])
def postQuestion():
    value = request.json

    if ((not request.json) or (not "ref" in request.json) or (not "option_type" in request.json) or (not "area" in request.json) or (not "group" in request.json)):
        abort(400)

    ref = value["ref"]
    option_type = value["option_type"]
    area = value["area"]
    group = value["group"]

    areaAux = Area().get_area(area)
    groupAux = Group().get_group(group)
    stationAux = Station().get_station(groupAux.id_station)

    if((areaAux == False) or (groupAux==False) or (stationAux==False)):
        abort(404)

    if(areaAux.id_ecoe != stationAux.id_ecoe):
        abort(404)

    question = Question(ref, option_type, area, group)
    question.post_question()

    return "AAAAAA"

 #   return jsonify({
  #      "$ref": question,
   #     "$option_type": option_type,
    #    "$area": area,
     #   "$group": group
   # })

