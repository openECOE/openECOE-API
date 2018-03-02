from ws import *
from model import Group, Area, Question

@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['GET'])
def obtenPreguntas(grupo_id):
    grupo = Group().get_group(grupo_id)

    if (grupo):
        preguntas = []
        for pregunta in grupo.preguntas:
            preguntas.append({
                "id_pregunta" : pregunta.id_pregunta,
                "ref" : pregunta.ref,
                "tipo_opcion" : pregunta.tipo_opcion
            })

        return json.dumps(preguntas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['GET'])
def obtenPregunta(grupo_id, pregunta_id):
    grupo = Group().get_group(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Question().get_pregunta(pregunta_id)
            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_opcion" : pregunta.tipo_opcion})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['POST'])
def insertaPregunta(grupo_id):
    grupo = Group().get_group(grupo_id)

    if (grupo):
        value = request.json

        if ((not request.json) or (not "ref" in request.json) or (not "tipo_opcion" in request.json)):
            abort(400)

        ref = value["ref"]
        tipo_opcion = value["tipo_opcion"]

        preguntaIn = Question(ref, tipo_opcion, grupo_id)
        preguntaIn.post_pregunta()

        pregunta = Question().get_ult_pregunta()

        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_opcion": pregunta.tipo_opcion})

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['PUT'])
def modificaPregunta(grupo_id, pregunta_id):
    grupo = Group().get_group(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            value = request.json

            if ((not request.json) or (not "ref" in request.json) or (not "tipo_opcion" in request.json) or (not "id_grupo" in request.json)):
                abort(400)

            ref = value["ref"]
            tipo_opcion = value["tipo_opcion"]
            id_grupo = value["id_grupo"]

            pregunta = Question().get_pregunta(pregunta_id)
            pregunta.put_pregunta(ref, tipo_opcion, id_grupo)

            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_opcion" : pregunta.tipo_opcion})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['DELETE'])
def eliminaPregunta(grupo_id, pregunta_id):
    grupo = Group().get_group(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Question().get_pregunta(pregunta_id)
            pregunta.delete_pregunta()

            return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_opcion": pregunta.tipo_opcion})
        else:
            abort(404)

    else:
        abort(404)


# Relacion Pregunta-Area
@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['GET'])
def obtenAreaPregunta(pregunta_id):
    pregunta = Question().get_pregunta(pregunta_id)

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
    pregunta = Question().get_pregunta(pregunta_id)

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
    pregunta = Question().get_pregunta(pregunta_id)

    if(pregunta):
        area = pregunta.area
        pregunta.delete_pregunta_area()

        return jsonify({"id_area": area.id_area, "nombre": area.nombre})
    else:
        abort(404)