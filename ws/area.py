from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import ECOE, Area

def existEcoeArea(area, ecoe_id):
    if(area):
        if(area.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False


#ECOE-Area
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/area/', methods=['GET'])
def getAreas(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        areas = []
        for area in ecoe.areas:
            areas.append({
                "id_area" : area.id_area,
                "name" : area.name
        })

        return json.dumps(areas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/area/<int:area_id>/', methods=['GET'])
def obtenArea(ecoe_id, area_id):

    area = Area().get_area(area_id)

    if(existEcoeArea(area, ecoe_id)==False):
        abort(404)

    return jsonify({"id_area": area.id_area, "name": area.name})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/area/', methods=['POST'])
def postArea(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if not request.json or not "name" in request.json:
            abort(400)

        name = value["name"]

        areaIn = Area(name=name, id_ecoe=ecoe_id)
        areaIn.post_area()

        area = Area().get_last_area()

        return jsonify({"id_area" : area.id_area, "name" : area.name})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/area/<int:area_id>/', methods=['PUT'])
def putArea(ecoe_id, area_id):

   area = Area().get_area(area_id)

   if (existEcoeArea(area, ecoe_id) == False):
    abort(404)

    value = request.json

    if ((not request.json) or (not "name" in request.json) or (not "id_ecoe" in request.json)):
        abort(400)

    name = value["name"]
    id_ecoe = value["id_ecoe"]

    area = Area().get_area(area_id)
    area.put_area(name, id_ecoe)

    return jsonify({"id_area": area.id_area, "name": area.name})




@app.route('/api/v1.0/ECOE/<int:ecoe_id>/area/<int:area_id>/', methods=['DELETE'])
def eliminaArea(ecoe_id, area_id):
    area = Area().get_area(area_id)

    if (existEcoeArea(area, ecoe_id) == False):
        abort(404)

    area = Area().get_area(area_id)
    area.delete_area()

    return jsonify({"id_area": area.id_area, "nombre": area.name})

