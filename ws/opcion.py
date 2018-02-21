from ws import *
from model import Pregunta, Opcion

#RUTAS DE OPCION
@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['GET'])
def muestraOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(pregunta):
        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones', methods=['POST'])
def insertaOpcion(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):

            puntos = value["puntos"]
            descripcion = value["descripcion"]

            opcionIn = Opcion(puntos=puntos, descripcion=descripcion)
            opcionIn.post_opcion()

            opcion = Opcion().get_ult_opcion()

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['PUT'])
def modificaOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):

            puntos = value["puntos"]
            descripcion = value["descripcion"]

            opcion.put_opcion(puntos, descripcion)

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['DELETE'])
def eliminaOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(opcion):
        opcion.delete_opcion()
        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)