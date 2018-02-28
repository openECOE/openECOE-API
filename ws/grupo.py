from ws import *
from model import Station, Grupo

# Relacion Estacion-Grupos
@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/', methods=['GET'])
def obtenGrupos(estacion_id):
    estacion = Station().get_estacion(estacion_id)

    if (estacion):
        grupos = []
        for grupo in estacion.grupos:
            grupos.append({
                "id_grupo": grupo.id_grupo,
                "nombre": grupo.nombre
            })

        return json.dumps(grupos, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['GET'])
def obtenGrupo(estacion_id, grupo_id):
    estacion = Station().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos()):
            grupo = Grupo().get_grupo(grupo_id)
            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/', methods=['POST'])
def insertaGrupo(estacion_id):
    estacion = Station().get_estacion(estacion_id)

    if (estacion):

        value = request.json

        if ((not request.json) or (not "nombre" in request.json)):
            abort(400)

        nombre = value["nombre"]

        grupoIn = Grupo(nombre=nombre, id_estacion=estacion_id)
        grupoIn.post_grupo()

        grupo = Grupo().get_ult_grupo()

        return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['PUT'])
def modificaGrupo(estacion_id, grupo_id):
    estacion = Station().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos(grupo_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_estacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_estacion = value["id_estacion"]

            grupo = Grupo().get_grupo(grupo_id)
            grupo.put_grupo(nombre, id_estacion)

            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['DELETE'])
def eliminaGrupo(estacion_id, grupo_id):
    estacion = Station().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos(grupo_id)):
            grupo = Grupo().get_grupo(grupo_id)
            grupo.delete_grupo()

            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)
