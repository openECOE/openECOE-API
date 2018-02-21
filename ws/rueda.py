from ws import *
from model import Turno, Rueda

# RUTAS DE RUEDA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas/<int:rueda_id>', methods=['GET'])
def muestraRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)
    rueda = Rueda().get_rueda(rueda_id)

    if(turno):
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})

    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas', methods=['POST'])
def insertaRueda(turno_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        value = request.json
        if ((not request.json) or (not "descripcion" in request.json)):

            descripcion = value["descripcion"]

            ruedaIn = Rueda(descripcion=descripcion, id_turno=turno_id)
            ruedaIn.post_rueda()

        rueda = Rueda().get_ult_rueda()

        return jsonify({"id_rueda":rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas/<int:rueda_id>', methods=['PUT'])
def modificaRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)
    rueda = Rueda().get_rueda(rueda_id)

    if(turno):
        value = request.json
        if ((not request.json) or (not "descripcion" in request.json)):

            descripcion = value["descripcion"]

            rueda.put_rueda(descripcion)

        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas/<int:rueda_id>', methods=['DELETE'])
def eliminaRueda(turno_id, rueda_id):
    turno = Turno().get_turno(turno_id)
    rueda = Rueda().get_rueda(rueda_id)

    if(turno):
        rueda.delete_rueda()
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)