from db import db
from db import app

from Organizacion import Organizacion
from Usuario import Usuario

from flask import Flask, jsonify, request

from werkzeug.exceptions import abort, Response


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['GET'])
def muestraUsuariosOrg(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        usuarios = []

        for usuario in organizacion.usuarios.all():
            usuarios.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellidos": usuario.apellidos,
                "id_organizacion": usuario.id_organizacion,
            })

        return jsonify(usuarios)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['GET'])
def muestraUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        for usuario in organizacion.usuarios.all():
            if usuario_id == usuario.id_usuario:
                usuario = Usuario().get_usuario(usuario_id)
                return jsonify(
                    {"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos,
                     "id_organizacion": usuario.id_organizacion})
        abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['POST'])
def insertaUsuarioOrg(organizacion_id):
    value = request.json
    nombre = value["nombre"]
    apellidos = value["apellidos"]

    usuarioIn = Usuario(nombre, apellidos, organizacion_id)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos, "id_organizacion" : usuario.id_organizacion})


