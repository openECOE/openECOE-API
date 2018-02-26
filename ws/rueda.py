from ws import *
from model import Turno, Rueda

# RUTAS DE TURNO
@app.route('/api/v1.0/turnos/<int:turno_id>/ruedas/', methods=['GET'])
def muestraRuedas(turno_id):
    turno = Turno().get_turno(turno_id)

    if (turno):
        ruedas = []

        for rueda in turno.ruedas:
            ruedas.append({
                "id_rueda": rueda.id_rueda,
                "descripcion": rueda.descripcion
            })

        return json.dumps(ruedas, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


# RUTAS DE RUEDA
@app.route('/api/v1.0/turnos/<int:turno_id>/ruedas/<int:rueda_id>/', methods=['GET'])
def muestraRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        if(turno.existe_turno_rueda(rueda_id)==False):
            abort(404)

        rueda = Rueda().get_rueda(rueda_id)
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})

    else:
        abort(404)



@app.route('/api/v1.0/turnos/<int:turno_id>/ruedas/', methods=['POST'])
def insertaRueda(turno_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        value = request.json
        if ((not request.json) or (not "descripcion" in request.json)):
            abort(400)

        descripcion = value["descripcion"]

        ruedaIn = Rueda(descripcion=descripcion, id_turno=turno_id)
        ruedaIn.post_rueda()

        rueda = Rueda().get_ult_rueda()

        return jsonify({"id_rueda":rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/turnos/<int:turno_id>/ruedas/<int:rueda_id>/', methods=['PUT'])
def modificaRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        if(turno.existe_turno_rueda(rueda_id)==False):
            abort(404)

        value = request.json

        if ((not request.json) or (not "descripcion" in request.json) or (not "id_turno" in request.json)):
            abort(400)

        descripcion = value["descripcion"]
        id_turno = value["id_turno"]

        rueda = Rueda().get_rueda(rueda_id)
        rueda.put_rueda(descripcion, id_turno)

        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/turnos/<int:turno_id>/ruedas/<int:rueda_id>/', methods=['DELETE'])
def eliminaRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)


    if(turno):
        if (turno.existe_turno_rueda(rueda_id) == False):
            abort(404)

        rueda = Rueda().get_rueda(rueda_id)
        rueda.delete_rueda()
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)