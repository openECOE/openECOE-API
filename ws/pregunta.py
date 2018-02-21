from ws import *
from model import Grupo, Area

@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['GET'])
def obtenPreguntas(grupo_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        preguntas = []
        for pregunta in grupo.preguntas:
            preguntas.append({
                "id_pregunta" : pregunta.id_pregunta,
                "ref" : pregunta.ref,
                "tipo_pregunta" : pregunta.tipo_pregunta
            })

        return json.dumps(preguntas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['GET'])
def obtenPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Pregunta().get_pregunta(pregunta_id)
            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_pregunta" : pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['POST'])
def insertaPregunta(grupo_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        value = request.json

        if ((not request.json) or (not "ref" in request.json) or (not "tipo_pregunta" in request.json)):
            abort(400)

        ref = value["ref"]
        tipo_pregunta = value["tipo_pregunta"]

        preguntaIn = Pregunta(ref, tipo_pregunta, grupo_id)
        preguntaIn.post_pregunta()

        pregunta = Pregunta().get_ult_pregunta()

        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_pregunta": pregunta.tipo_pregunta})

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['PUT'])
def modificaPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            value = request.json

            if ((not request.json) or (not "ref" in request.json) or (not "tipo_pregunta" in request.json) or (not "id_grupo" in request.json)):
                abort(400)

            ref = value["ref"]
            tipo_pregunta = value["tipo_pregunta"]
            id_grupo = value["id_grupo"]

            pregunta = Pregunta().get_pregunta(pregunta_id)
            pregunta.put_pregunta(ref, tipo_pregunta, id_grupo)

            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_pregunta" : pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['DELETE'])
def eliminaPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Pregunta().get_pregunta(pregunta_id)
            pregunta.delete_pregunta()

            return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_pregunta": pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


# Relacion Pregunta-Area
@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['GET'])
def obtenAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if (pregunta):
        area = pregunta.area
        if(area):
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['PUT'])
def insertaAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if (pregunta):
        value = request.json

        if not request.json or not "id_area" in request.json:
            abort(400)

        id_area = value["id_area"]

        if(pregunta.existe_pregunta_id_ecoe(id_area)):
            pregunta.put_pregunta_area(id_area)
            area = pregunta.area

            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['DELETE'])
def eliminaAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        area = pregunta.area
        pregunta.delete_pregunta_area()

        return jsonify({"id_area": area.id_area, "nombre": area.nombre})
    else:
        abort(404)