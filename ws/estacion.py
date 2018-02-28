from ws import *
from model import ECOE, Station

def existEcoeAStation(station, ecoe_id):
    if(station):
        if(station.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False

#Relacion ECOE-Estacion
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/', methods=['GET'])
def obtenEstaciones(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        estaciones = []
        for estacion in ecoe.estaciones:
            estaciones.append({
                "id_estacion" : estacion.id_estacion,
                "nombre" : estacion.nombre
        })

        return json.dumps(estaciones, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<int:estacion_id>/', methods=['GET'])
def obtenEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Station().get_estacion(estacion_id)
            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/', methods=['POST'])
def insertaEstacion(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json)):
            abort(400)

        nombre = value["nombre"]

        cronometros = ecoe.cronometros

        estacionIn = Station(nombre, ecoe_id, cronometros)
        estacionIn.post_estacion()

        estacion = Station().get_ult_estacion()

        return jsonify({"id_estacion" : estacion.id_estacion, "nombre" : estacion.nombre})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<int:estacion_id>/', methods=['PUT'])
def modificaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_ecoe = value["id_ecoe"]

            estacion = Station().get_estacion(estacion_id)
            estacion.put_estacion(nombre, id_ecoe)

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/station/<int:estacion_id>/', methods=['DELETE'])
def eliminaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Station().get_estacion(estacion_id)
            estacion.delete_estacion()

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)
