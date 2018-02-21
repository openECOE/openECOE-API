from ws import *
from model import ECOE, Dia

# RUTAS DE DIA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['GET'])
def muestraDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    dia = Dia().get_dia(dia_id)

    if (ecoe):

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias', methods=['POST'])
def insertaDia(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        value = request.json

        # comprobar json
        if ((not request.json) or (not "fecha" in request.json)):
            fecha = value["fecha"]

            diaIn = Dia(fecha=fecha, id_ecoe=ecoe_id)
            diaIn.post_dia()

            dia = Dia().get_ult_dia()

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['PUT'])
def modificaDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)
    dia = Dia().get_dia(dia_id)

    if (ecoe):
        value = request.json
        fecha = value["fecha"]

        dia.put_dia(fecha)

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['DELETE'])
def eliminaDia(ecoe_id, dia_id):
    ecoe = ECOE().get_ECOE(ecoe_id)
    dia = Dia().get_dia(dia_id)

    if (ecoe):
        dia.delete_dia()
        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)

