from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import Organization, ECOE

#Rutas de Organizacion-ECOE
@app.route('/api/v1.0/organization/<int:organizacion_id>/ECOE/', methods=['GET'])
def muestraEcoesOrganizacion(organizacion_id):
    organizacion = Organization().get_organization(organizacion_id)

    ecoes=[]

    if(organizacion):
        for ecoe in organizacion.ecoes:
            ecoes.append({
                "id" : ecoe.id,
                "nombre" : ecoe.nombre,
            })

        return json.dumps(ecoes, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['GET'])
def muestraEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organization().get_organization(organizacion_id)

    if(organizacion):
        if(organizacion.exist_organization_ecoe(ecoe_id)):
            ecoe = ECOE().get_ECOE(ecoe_id)
            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/ECOE/', methods=['POST'])
def creaEcoeOrganizacion(organizacion_id):
    organizacion = Organization().get_organization(organizacion_id)
    if(organizacion):
        value = request.json

        if not request.json or not "nombre" in request.json:
            abort(400)

        nombre = value["nombre"]

        ecoe = ECOE(nombre, organizacion_id)
        ecoe.post_ecoe()

        return jsonify({"id": ecoe.id, "nombre": ecoe.name})
    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['PUT'])
def modificaEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organization().get_organization(organizacion_id)

    if(organizacion):
        if(organizacion.exist_organization_ecoe(ecoe_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_organizacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_organizacion = value["id_organizacion"]

            ecoe = ECOE().get_ECOE(ecoe_id)
            ecoe.put_ecoe(nombre, id_organizacion)

            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)




@app.route('/api/v1.0/organization/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['DELETE'])
def eliminaEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organization().get_organization(organizacion_id)

    if (organizacion):
        if (organizacion.exist_organization_ecoe(ecoe_id)):

            ecoe = ECOE().get_ECOE(ecoe_id)
            ecoe.delete_ecoe()

            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)
