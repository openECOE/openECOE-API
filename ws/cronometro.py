from ws import *
from model import Estacion, Cronometro

#Relacion Estacion-Cronometro
@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['GET'])
def obtenCronometros(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

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
def obtenCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total" : cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['POST'])
def insertaCronometro(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
            abort(400)

        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometroIn = Cronometro(nombre, tiempo_total, estacion_id)
        cronometroIn.post_cronometro()

        cronometro = Cronometro().get_ult_cronometro()

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['PUT'])
def modificaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json) or (not "id_estacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            tiempo_total = value["tiempo_total"]
            id_estacion = value["id_estacion"]

            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.put_cronometro(nombre, tiempo_total, id_estacion)

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.delete_cronometro()

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)
