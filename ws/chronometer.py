from model import Chronometer, ECOE, Station

from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort


#API Cronometro
@app.route('/api/v1.0/cronometros/', methods=['GET'])
def muestraCronometros():
    cronometros = []

    for cronometro in Chronometer.query.all():
        cronometros.append({
            "id_cronometro": cronometro.id_cronometro,
            "nombre": cronometro.nombre,
            "tiempo_total": cronometro.tiempo_total
        })

    return json.dumps(cronometros, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/', methods=['GET'])
def muestraCronometro(cronometro_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if(cronometro):
        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/cronometros/', methods=['POST'])
def insertaCronometro():
    value = request.json

    if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
        abort(400)

    nombre = value["nombre"]
    tiempo_total = value["tiempo_total"]

    cronometroIn = Chronometer(nombre, tiempo_total)
    cronometroIn.post_cronometro()

    cronometro = Chronometer().get_ult_cronometro()
    return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})


@app.route('/api/v1.0/cronometros/<int:cronometro_id>/', methods=['PUT'])
def actualizaCronometro(cronometro_id):
    cronometro = Chronometer().get_ult_cronometro()

    if(cronometro):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
            abort(400)

        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometro = Chronometer().get_cronometro(cronometro_id)
        cronometro.put_cronometro(nombre, tiempo_total)

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
      abort(404)


@app.route('/api/v1.0/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometro(cronometro_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        cronometro.delete_cronometro()
        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)


#Relacion ECOE-Cronometro
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/cronometros/', methods=['GET'])
def obtenCronometrosEcoe(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        cronometros = []
        for cronometro in ecoe.cronometros:
            cronometros.append({
                "id_cronometro": cronometro.id_cronometro,
                "nombre": cronometro.nombre,
                "tiempo_total": cronometro.tiempo_total
            })

        return json.dumps(cronometros, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/cronometros/<int:cronometro_id>/', methods=['GET'])
def obtenCronometroEcoe(ecoe_id, cronometro_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.exists_ecoe_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)
            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total" : cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/cronometros/', methods=['POST'])
def insertaCronometroEcoe(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
            abort(400)

        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometroIn = Chronometer(nombre, tiempo_total)
        cronometroIn.post_cronometro()

        cronometro = Chronometer().get_ult_cronometro()
        ecoe.put_ecoe_chronometer(cronometro)

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/cronometros/<int:cronometro_id>/', methods=['PUT'])
def modificaCronometroEcoe(ecoe_id, cronometro_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.exists_ecoe_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)

            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
                abort(400)

            nombre = value["nombre"]
            tiempo_total = value["tiempo_total"]

            cronometro.put_cronometro(nombre, tiempo_total)

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(405)

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometroEcoe(ecoe_id, cronometro_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.exists_ecoe_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)
            cronometro.delete_cronometro()

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)


#Relacion Estacion-Cronometro
@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['GET'])
def obtenCronometrosEstacion(estacion_id):
    estacion = Station().get_station(estacion_id)

    if (estacion):
        cronometros = []
        for cronometro in estacion.cronometros:
            cronometros.append({
                "id_cronometro": cronometro.id_cronometro,
                "nombre": cronometro.nombre,
                "tiempo_total": cronometro.tiempo_total
            })

        return json.dumps(cronometros, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['GET'])
def obtenCronometroEstacion(estacion_id, cronometro_id):
    estacion = Station().get_station(estacion_id)

    if (estacion):
        if (estacion.exists_station_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)
            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total" : cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['POST'])
def insertaCronometroEstacion(estacion_id):
    estacion = Station().get_station(estacion_id)

    if (estacion):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
            abort(400)

        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometroIn = Chronometer(nombre, tiempo_total)
        cronometroIn.post_cronometro()

        cronometro = Chronometer().get_ult_cronometro()
        estacion.put_station_chronometer(cronometro)

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['PUT'])
def modificaCronometroEstacion(estacion_id, cronometro_id):
    estacion = Station().get_station(estacion_id)

    if (estacion):
        if (estacion.exists_station_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)

            value = request.json

            nombre = value["nombre"]
            tiempo_total = value["tiempo_total"]

            cronometro.put_cronometro(nombre, tiempo_total)

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(405)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometroEstacion(estacion_id, cronometro_id):
    estacion = Station().get_station(estacion_id)

    if (estacion):
        if (estacion.exists_station_chronometer(cronometro_id)):
            cronometro = Chronometer().get_cronometro(cronometro_id)
            cronometro.delete_cronometro()

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)
