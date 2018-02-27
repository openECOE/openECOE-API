from ws import *
from model import Permiso, Usuario

@app.route('/api/v1.0/permission/', methods=['GET'])
def muestraPermisos():
    permisos = []

    for permiso in Permiso.query.all():
        permisos.append({
            "id_permiso": permiso.id_permiso,
            "id_tipoPermiso": permiso.id_tipoPermiso,
            "id_organizacion": permiso.id_organizacion,
            "id_ecoe": permiso.id_ecoe,
            "id_estacion": permiso.id_estacion
        })

    return json.dumps(permisos, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/permission/<int:permiso_id>/', methods=['GET'])
def muestraPermiso(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if(permiso):
        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)

@app.route('/api/v1.0/permission/', methods=['POST'])
def insertaPermiso():
    value = request.json

    if ((not request.json) or (not "id_tipoPermiso" in request.json) or (not "id_organizacion" in request.json) or (not "id_ecoe" in request.json) or (not "id_estacion" in request.json)):
        abort(400)

    id_tipoPermiso = value["id_tipoPermiso"]
    id_organizacion = value["id_organizacion"]
    id_ecoe = value["id_ecoe"]
    id_estacion = value["id_estacion"]

    permisoIn = Permiso(id_tipoPermiso, id_organizacion, id_ecoe, id_estacion)
    permisoIn.post_permiso()

    permiso = Permiso().get_ult_permiso()
    return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})


@app.route('/api/v1.0/permission/<int:permiso_id>/', methods=['PUT'])
def actualizaPermiso(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if(permiso):
        value = request.json

        if ((not request.json) or (not "id_tipoPermiso"  in request.json) or (not "id_organizacion" in request.json) or (not "id_ecoe" in request.json) or (not "id_estacion" in request.json)):
            abort(400)

        id_tipoPermiso = value["id_tipoPermiso"]
        id_organizacion = value["id_organizacion"]
        id_ecoe = value["id_ecoe"]
        id_estacion = value["id_estacion"]

        permiso = Permiso().get_permiso(permiso_id)
        permiso.put_permiso(id_tipoPermiso, id_organizacion, id_ecoe, id_estacion)

        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)


@app.route('/api/v1.0/permission/<int:permiso_id>/', methods=['DELETE'])
def eliminaPermiso(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if (permiso):
        permiso.delete_permiso()
        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)

#API Usuario-Permiso
@app.route('/api/v1.0/user/<int:usuario_id>/permission/', methods=['GET'])
def muestraPermisosUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        permisos = []

        for permiso in usuario.permisos:
            permisos.append({
                "id_permiso": permiso.id_permiso,
                "id_tipoPermiso": permiso.id_tipoPermiso,
                "id_organizacion": permiso.id_organizacion,
                "id_ecoe": permiso.id_ecoe,
                "id_estacion": permiso.id_estacion
            })

        return json.dumps(permisos, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/user/<int:usuario_id>/permission/<int:permiso_id>/', methods=['GET'])
def muestraUsuarioPerm(usuario_id, permiso_id):
    usuario = Usuario().get_usuario(usuario_id)

    if (usuario):
        if(usuario.existe_usuario_permiso(permiso_id)):
            permiso = Permiso().get_permiso(permiso_id)
            return jsonify({"id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion" : permiso.id_estacion})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/user/<int:usuario_id>/permission/', methods=['POST'])
def insertaUsuarioPerm(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json

        if ((not request.json) or (not "id_tipoPermiso"  in request.json) or (not "id_organizacion" in request.json) or (not "id_ecoe" in request.json) or (not "id_estacion" in request.json)):
            abort(400)

        id_tipoPermiso = value["id_tipoPermiso"]
        id_organizacion = value["id_organizacion"]
        id_ecoe = value["id_ecoe"]
        id_estacion = value["id_estacion"]


        permisoIn = Permiso(id_tipoPermiso, id_organizacion, id_ecoe, id_estacion)
        permisoIn.post_permiso()

        permiso = Permiso().get_ult_permiso()
        usuario.put_usuario_permisos(permiso)

        return jsonify({"id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})

    else:
        abort(404)


@app.route('/api/v1.0/user/<int:usuario_id>/permission/<int:permiso_id>/', methods=['PUT'])
def anyadeUsuarioPerm(usuario_id, permiso_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        permiso = Permiso().get_permiso(permiso_id)
        if(permiso):
            if(usuario.existe_usuario_permiso(permiso_id)==False):
                usuario.put_usuario_permisos(permiso)
                return jsonify({"id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
            else:
                abort(405)

        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/user/<int:usuario_id>/permission/<int:permiso_id>/', methods=['DELETE'])
def eliminaUsuarioPerm(usuario_id, permiso_id):
    usuario = Usuario().get_usuario(usuario_id)
    if(usuario):
        if(usuario.existe_usuario_permiso(permiso_id)):
            permiso = Permiso().get_permiso(permiso_id)
            usuario.delete_usuario_permiso(permiso)

            return jsonify({"id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
        else:
            abort(404)
    else:
        abort(404)