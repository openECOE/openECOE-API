from ws import app
from model import ECOE, Chronometer, Alarm
from flask import jsonify, request, abort, json

def existEcoeCrono(ecoe_id, crono_id):
    ecoe = ECOE().get_ECOE(ecoe_id)
    if (ecoe == False):
        return False

    if (ecoe.exists_ecoe_chronometer(crono_id) == False):
        return False

    return True



@app.route('/api/v1.0/ECOE/<ecoe_id>/chrono/<int:cronometro_id>/alarm/', methods=['GET'])
def getAlarms(ecoe_id, cronometro_id):
    if (existEcoeCrono(ecoe_id, cronometro_id) == False):
        abort(404)

    cronometro = Chronometer().get_cronometro(cronometro_id)

    alarmas = []
    for alarma in cronometro.alarmas:
        alarmas.append({
            "id_alarma": alarma.id_alarma,
            "tiempo": alarma.tiempo,
            "sonido": alarma.sonido
        })

    return json.dumps(alarmas, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/ECOE/<ecoe_id>/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['GET'])
def getAlarm(ecoe_id, cronometro_id, alarma_id):
    if (existEcoeCrono(ecoe_id, cronometro_id) == False):
        abort(404)

    cronometro = Chronometer().get_cronometro(cronometro_id)
    if(cronometro.existe_cronometro_alarma()):
        abort(404)
    alarma = Alarm().get_alarma(alarma_id)

    return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})


@app.route('/api/v1.0/ECOE/<ecoe_id>/chrono/<int:cronometro_id>/alarm/', methods=['POST'])
def postAlarm(ecoe_id, cronometro_id):
    if (existEcoeCrono(ecoe_id, cronometro_id) == False):
        abort(404)

    value = request.json

    if ((not request.json) or (not "tiempo" in request.json) or (not "sonido" in request.json) or (not "id_cronometro" in request.json)):
        abort(400)

    tiempo = value["tiempo"]
    sonido = value["sonido"]

    alarmaIn = Alarm(tiempo, sonido, cronometro_id)
    alarmaIn.post_alarma()

    alarma = Alarm().get_ult_alarma()

    return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})


@app.route('/api/v1.0/ECOE/<ecoe_id>/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['PUT'])
def putAlarm(ecoe_id, cronometro_id, alarma_id):
    if (existEcoeCrono(ecoe_id, cronometro_id) == False):
        abort(404)

    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro.existe_cronometro_alarma(alarma_id)):
        value = request.json

        if ((not request.json) or (not "tiempo" in request.json)  or (not "sonido" in request.json) (not "id_cronometro" in request.json)):
            abort(400)

        tiempo = value["tiempo"]
        sonido = value["sonido"]
        id_cronometro = value["id_cronometro"]

        alarma = Alarm().get_alarma(alarma_id)
        alarma.put_alarma(tiempo, sonido, id_cronometro)

        return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<ecoe_id>/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['DELETE'])
def delAlarm(ecoe_id, cronometro_id, alarma_id):
    if (existEcoeCrono(ecoe_id, cronometro_id) == False):
        abort(404)

    cronometro = Chronometer().get_cronometro(cronometro_id)
    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            alarma = Alarm().get_alarma(alarma_id)
            alarma.delete_alarma()

            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/chrono/<int:cronometro_id>/alarm/', methods=['GET'])
def obtenAlarmas(cronometro_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        alarmas = []
        for alarma in cronometro.alarmas:
            alarmas.append({
                "id_alarma": alarma.id_alarma,
                "tiempo": alarma.tiempo,
                "sonido": alarma.sonido
            })

        return json.dumps(alarmas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['GET'])
def obtenAlarma(cronometro_id, alarma_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        alarma = Alarm().get_alarma(alarma_id)
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/chrono/<int:cronometro_id>/alarm/', methods=['POST'])
def insertaAlarma(cronometro_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        value = request.json

        if ((not request.json) or (not "tiempo" in request.json) or (not "sonido" in request.json) or (not "id_cronometro" in request.json)):
            abort(400)

        tiempo = value["tiempo"]
        sonido = value["sonido"]



        alarmaIn = Alarm(tiempo, sonido, cronometro_id)
        alarmaIn.post_alarma()

        alarma = Alarm().get_ult_alarma()

        return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
    else:
        abort(404)

@app.route('/api/v1.0/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['PUT'])
def modificaAlarma(cronometro_id, alarma_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            value = request.json

            if ((not request.json) or (not "tiempo" in request.json)  or (not "sonido" in request.json) (not "id_cronometro" in request.json)):
                abort(400)

            tiempo = value["tiempo"]
            sonido = value["sonido"]
            id_cronometro = value["id_cronometro"]

            alarma = Alarm().get_alarma(alarma_id)
            alarma.put_alarma(tiempo, sonido, id_cronometro)

            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/chrono/<int:cronometro_id>/alarm/<int:alarma_id>/', methods=['DELETE'])
def eliminaAlarma(cronometro_id, alarma_id):
    cronometro = Chronometer().get_cronometro(cronometro_id)

    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            alarma = Alarm().get_alarma(alarma_id)
            alarma.delete_alarma()

            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)
