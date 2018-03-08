from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import ECOE, Station

def existEcoeAStation(station, ecoe_id):
    if(station):
        if(station.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False

#Relacion ECOE-Estacion
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/', methods=['GET'])
def getStations(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        stations = []
        for station in ecoe.stations:
            stations.append({
                "id_station" : station.id_station,
                "name" : station.name
        })

        return json.dumps(stations, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/', methods=['GET'])
def getStation(ecoe_id, station_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_estacion(station_id)):
            station = Station().get_station(station_id)
            return jsonify({"id_station": station.id_station, "name": station.name})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/', methods=['POST'])
def postStation(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "name" in request.json)):
            abort(400)

        name = value["name"]

        chronometers = ecoe.chronometers

        stationIn = Station(name, ecoe_id, chronometers)
        stationIn.post_station()

        station = Station().get_last_station()

        return jsonify({"id_station" : station.id_station, "name" : station.name})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/', methods=['PUT'])
def putStation(ecoe_id, station_id):
    station = Station().get_station(station_id)

    if (station):
        if (ecoe_id == station.id_ecoe):
            value = request.json

            if ((not request.json) or (not "name" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            name = value["name"]
            id_ecoe = value["id_ecoe"]

            station.put_station(name, id_ecoe)

            return jsonify({"id_station": station.id_station, "name": station.name, "id_ecoe": station.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<int:estacion_id>/', methods=['DELETE'])
def delStation(ecoe_id, estacion_id):
    station = Station().get_station(estacion_id)

    if (station):
        if (ecoe_id == station.id_ecoe):
            station.delete_station()

            return jsonify({"id_station": station.id_station, "name": station.name, "id_ecoe": station.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)
