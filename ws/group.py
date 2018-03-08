from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import Station, Group

def existGroupStation(group, station_id, ecoe_id):
    if(group):
        if(group.id_station == station_id):
            station = Station().get_station(station_id)

            if(existStationEcoe(station, ecoe_id)):
                return True
            else:
                return False

        else:
            return False
    else:
        return False

def existStationEcoe(station, ecoe_id):
    if (station):
        if (station.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False

# Relacion Estacion-Grupos
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/groups/', methods=['GET'])
def getGroups(ecoe_id, station_id):
    station = Station().get_station(station_id)

    if (existStationEcoe(station, ecoe_id)):
        groups = []
        for group in station.groups:
            groups.append({
                "id_group": group.id_group,
                "name": group.name
            })

        return json.dumps(groups, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/groups/<int:group_id>/', methods=['GET'])
def getGroup(ecoe_id, station_id, group_id):
    group = Group().get_group(group_id)

    if (existGroupStation(group, station_id, ecoe_id)):
        return jsonify({"id_grupo": group.id_group, "nombre": group.name})
    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/groups/', methods=['POST'])
def postGroup(ecoe_id, station_id):
    station = Station().get_station(station_id)

    if (existStationEcoe(station, ecoe_id)):

        value = request.json

        if ((not request.json) or (not "name" in request.json)):
            abort(400)

        name = value["name"]

        groupIn = Group(name=name, id_station=station_id)
        groupIn.post_group()

        group = Group().get_last_group()

        return jsonify({"id_grupo": group.id_group, "name": group.name})

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/groups/<group_id>/', methods=['PUT'])
def putGroup(ecoe_id, station_id, group_id):
    group = Group().get_group(group_id)

    if(existGroupStation(group, station_id, ecoe_id)):
        value = request.json

        if ((not request.json) or (not "name" in request.json) or (not "id_station" in request.json)):
            abort(400)

        name = value["name"]
        id_station = value["id_station"]

        group = Group().get_group(group_id)
        group.put_group(name, id_station)

        return jsonify({"id_grupo": group.id_group, "name": group.name})


    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<station_id>/groups/<int:grupo_id>/', methods=['DELETE'])
def delGroup(ecoe_id, station_id, group_id):
    group = Group().get_group(group_id)

    if (existGroupStation(group, station_id, ecoe_id)):
        group.delete_grupo()

        return jsonify({"id_grupo": group.id_group, "nombre": group.name})

    else:
        abort(404)
