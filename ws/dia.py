from ws import *
from model import ECOE, Dia

# RUTAS DE DIA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/', methods=['GET'])
def muestraDias(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        dias = []

        for dia in ecoe.dias:
            dias.append({
                "id_dia" : dia.id_dia,
                "fecha" : dia.fecha.strftime("%Y-%m-%d")
            })

        return json.dumps(dias, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/', methods=['GET'])
def muestraDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    dia = Dia().get_dia(dia_id)

    if (ecoe):

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha.strftime("%Y-%m-%d")})

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/', methods=['POST'])
def insertaDia(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        value = request.json

        # comprobar json
        if ((not request.json) or (not "fecha" in request.json)):
            abort(400)

        fecha = value["fecha"]

        diaIn = Dia(fecha=fecha, id_ecoe=ecoe_id)
        diaIn.post_dia()

        dia = Dia().get_ult_dia()

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha.strftime("%Y-%m-%d")})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/', methods=['PUT'])
def modificaDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_dias(dia_id) == False):
            abort(404)

        dia = Dia().get_dia(dia_id)

        value = request.json

        if ((not request.json) or (not "fecha" in request.json) or (not "id_ecoe" in request.json)):
            abort(400)

        fecha = value["fecha"]
        id_ecoe = value["id_ecoe"]

        dia.put_dia(fecha, id_ecoe)

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha.strftime("%Y-%m-%d")})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/', methods=['DELETE'])
def eliminaDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_dias(dia_id) == False):
            abort(400)

        dia = Dia().get_dia(dia_id)
        dia.delete_dia()
        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha.strftime("%Y-%m-%d")})
    else:
        abort(404)

