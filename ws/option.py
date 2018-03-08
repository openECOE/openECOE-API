from ws import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import Question, Option

#RUTAS DE OPCION
@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/', methods=['GET'])
def muestraOpciones(pregunta_id):
    pregunta = Question().get_pregunta(pregunta_id)

    if (pregunta):
        opciones = []
        for opcion in pregunta.opciones:
            opciones.append({
                "id_opcion" : opcion.id_opcion,
                "puntos" : opcion.puntos,
                "descripcion" : opcion.descripcion
            })

        return json.dumps(opciones, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)



@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>/', methods=['GET'])
def muestraOpcion(pregunta_id, opcion_id):
    pregunta = Question().get_pregunta(pregunta_id)

    if(pregunta):
        if(pregunta.existe_pregunta_opcion(opcion_id)==False):
            abort(404)

        opcion = Option().get_opcion(opcion_id)
        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})

    else:
        abort(404)

@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/', methods=['POST'])
def insertaOpcion(pregunta_id):
    pregunta = Question().get_pregunta(pregunta_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):
            abort(400)
        puntos = value["puntos"]
        descripcion = value["descripcion"]

        opcionIn = Option(puntos=puntos, descripcion=descripcion, id_pregunta=pregunta_id)
        opcionIn.post_opcion()

        opcion = Option().get_ult_opcion()

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>/', methods=['PUT'])
def modificaOpcion(pregunta_id, opcion_id):
    pregunta = Question().get_pregunta(pregunta_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):
            abort(400)

        puntos = value["puntos"]
        descripcion = value["descripcion"]
        id_pregunta = value["id_pregunta"]

        if(pregunta.existe_pregunta_opcion(opcion_id) == False):
            abort(400)

        opcion = Option().get_opcion(opcion_id)
        opcion.put_opcion(puntos, descripcion, id_pregunta)

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>/', methods=['DELETE'])
def eliminaOpcion(pregunta_id, opcion_id):
    pregunta = Question().get_pregunta(pregunta_id)

    if(pregunta):
        if(pregunta.existe_pregunta_opcion(opcion_id) == False):
            abort(404)

        opcion = Option().get_opcion(opcion_id)
        opcion.delete_opcion()

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)