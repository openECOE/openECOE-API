from ws import *
from model import Usuario, Organizacion, Permiso

#API Usuario
@app.route('/api/v1.0/user/', methods=['GET'])
def muestraUsuarios():
    usuarios = []

    for usuario in Usuario.query.all():
        usuarios.append({
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
        })

    return json.dumps(usuarios, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/user/<int:usuario_id>/', methods=['GET'])
def muestraUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)

@app.route('/api/v1.0/user/', methods=['POST'])
def insertaUsuario():
    value = request.json

    if ((not request.json) or (not "nombre" in request.json) or (not "apellidos" in request.json)):
        abort(400)

    nombre = value["nombre"]
    apellidos = value["apellidos"]

    usuarioIn = Usuario(nombre, apellidos)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos})


@app.route('/api/v1.0/user/<int:usuario_id>/', methods=['PUT'])
def actualizaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json

        if ((not request.json) or (not "nombre"  in request.json) or (not "apellidos" in request.json)):
            abort(400)

        nombre = value["nombre"]
        apellidos = value["apellidos"]

        usuario = Usuario().get_usuario(usuario_id)

        usuario.put_usuario(nombre, apellidos)

        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
      abort(404)


@app.route('/api/v1.0/user/<int:usuario_id>/', methods=['DELETE'])
def eliminaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if (usuario):
        usuario.delete_usuario()
        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)


#Rutas de Organizacion-Usuarios
@app.route('/api/v1.0/organization/<int:organizacion_id>/user/', methods=['GET'])
def muestraUsuariosOrg(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        usuarios = []

        for usuario in organizacion.usuarios:
            usuarios.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellidos": usuario.apellidos
            })

        return json.dumps(usuarios, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/user/<int:usuario_id>/', methods=['GET'])
def muestraUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        if(organizacion.existe_organizacion_usuario(usuario_id)):
            usuario = Usuario().get_usuario(usuario_id)
            return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/user/', methods=['POST'])
def insertaUsuarioOrg(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if(organizacion):
        value = request.json

        if ((not request.json) or (not "nombre"  in request.json) or (not "apellidos" in request.json)):
            abort(400)

        nombre = value["nombre"]
        apellidos = value["apellidos"]

        usuarioIn = Usuario(nombre, apellidos)
        usuarioIn.post_usuario()

        usuario = Usuario().get_ult_usuario()
        organizacion.put_organizacion_usuario(usuario)

        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)



@app.route('/api/v1.0/organization/<int:organizacion_id>/user/<int:usuario_id>/', methods=['PUT'])
def anyadeUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if(organizacion):
        usuario = Usuario().get_usuario(usuario_id)
        if(usuario):
            if (organizacion.existe_organizacion_usuario(usuario_id) == False):
                organizacion.put_organizacion_usuario(usuario)
                return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
            else:
                abort(405)
        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/organization/<int:organizacion_id>/user/<int:usuario_id>/', methods=['DELETE'])
def eliminaUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)
    if(organizacion):
        if(organizacion.existe_organizacion_usuario(usuario_id)):
            usuario = Usuario().get_usuario(usuario_id)
            organizacion.delete_organizacion_usuario(usuario)

            return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
        else:
            abort(404)
    else:
        abort(404)



#API Permiso-Usuario
@app.route('/api/v1.0/permission/<int:permiso_id>/user/', methods=['GET'])
def muestraPermisosUsu(permiso_id):

    permiso = Permiso().get_permiso(permiso_id)

    if(permiso):
        usuarios = Usuario().get_permiso_usuarios(permiso_id)
        estructura = []

        for usuario in usuarios:
            estructura.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellidos": usuario.apellidos
            })

        return json.dumps(estructura, indent=1, ensure_ascii=False).encode('utf8')

    else:
       abort(404)

