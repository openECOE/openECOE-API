from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from flask import jsonify
from werkzeug.exceptions import abort


import json

from app.api import bp

from app.model.Station import Station
from app.model.ECOE import ECOE

class StationResource(ModelResource):
    groups = Relation('group')

    class Meta:
        model = Station
        natural_key = ('name')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        chronometers = fields.ToMany('chronometer')

#@bp.route('/sta/<int:id>/chronometers', methods=['GET']):
#def getStations(id):
#    return True

# def outJsonStation(station, cod):
#
#     if(cod==0):
#         ecoe = ECOE().get_ECOE(station.id_ecoe)
#         classIn = ecoe
#     else:
#         classIn = station
#
#
#     myjson = {
#         "$uri": "/station/" + str(station.id_station),
#         "name": station.name,
#         "chronometers": outJsonChronometers(classIn),
#         "ecoe": {
#             "$ref": "/ecoe/" + str(station.id_ecoe)
#         }
#     }
#
#     return myjson
#
# def outJson(out):
#     myjson = jsonify(out)
#     return myjson
#
# def outJsonChronometer(chronometer):
#     return {"$ref": "/chronometer/" + str(chronometer.id_chronometer)}
#
# def outJsonChronometers(classIn):
#
#     classArr =[]
#
#     for chronometer in classIn.chronometers:
#         classArr.append(outJsonChronometer(chronometer))
#
#     return classArr
#
# @bp.route('/station', methods=['GET'])
# def getStations():
#     arrSta = []
#
#     stations = Station().get_stations()
#
#     for station in stations:
#
#         if (len(station.chronometers) == 0):
#             cod =0
#         else:
#             cod = 1
#
#         arrSta.append(
#             outJsonStation(station, cod)
#         )
#
#     return json.dumps(arrSta, indent=1, ensure_ascii=False).encode('utf8')
#
#
# @bp.route('/station/<int:id>', methods=['GET'])
# def getStation(id):
#     station = Station().get_station(id)
#
#     if(station):
#         chronometers = station.chronometers
#
#         if(len(chronometers)==0):
#             return outJson(outJsonStation(station, 0))
#         else:
#             return outJson(outJsonStation(station, 1))
#
#     else:
#         abort(404)
