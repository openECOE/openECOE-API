from ws import *
from model import Dia, Turno

# RUTAS DE TURNO
@app.route('/api/v1.0/dias/<int:dia_id>/turnos/', methods=['GET'])
def muestraTurnos(dia_id):
    dia = Dia().get_dia(dia_id)

    if (dia):
        turnos = []

        for turno in dia.turnos:
            turnos.append({
                "id_turno": turno.id_turno,
                "hora_inicio": turno.hora_inicio.strftime("%H:%M")
            })

        return json.dumps(turnos, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


@app.route('/api/v1.0/dias/<int:dia_id>/turnos/<int:turno_id>/', methods=['GET'])
def muestraTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)
    turno = Turno().get_turno(turno_id)


    if(dia):
        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio.strftime("%H:%M")})

    else:
        abort(404)



@app.route('/api/v1.0/dias/<int:dia_id>/turnos/', methods=['POST'])
def insertaTurno(dia_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        value = request.json
        if ((not request.json) or (not "hora_inicio" in request.json)):
            abort(400)

        hora_inicio = value["hora_inicio"]

        turnoIn = Turno(hora_inicio=hora_inicio, id_dia=dia_id)
        turnoIn.post_turno()

        turno = Turno().get_ult_turno()

        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio.strftime("%H:%M")})
    else:
        abort(404)

@app.route('/api/v1.0/dias/<int:dia_id>/turnos/<int:turno_id>/', methods=['PUT'])
def modificaTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        value = request.json

        if ((not request.json) or (not "hora_inicio" in request.json) or (not "id_dia" in request.json)):
            abort(400)

        hora_inicio = value["hora_inicio"]
        id_dia = value["id_dia"]

        if(dia.existe_dia_turno(turno_id)==False):
            abort(404)

        turno = Turno().get_turno(turno_id)
        turno.put_turno(hora_inicio, id_dia)

        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio.strftime("%H:%M")})
    else:
        abort(404)

@app.route('/api/v1.0/dias/<int:dia_id>/turnos/<int:turno_id>/', methods=['DELETE'])
def eliminaTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        if(dia.existe_dia_turno(turno_id) == False):
            abort(404)
        turno = Turno().get_turno(turno_id)
        turno.delete_turno()
        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio.strftime("%H:%M")})
    else:
        abort(404)