from db import app
from db import db
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import abort, Response

import numpy as np
import json

from Permiso import Permiso

UsuPerm = db.Table('UsuPerm', db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True), db.Column('id_permiso', db.Integer, db.ForeignKey('permiso.id_permiso'), primary_key=True))


class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    permisos = db.relationship('Permiso', secondary=UsuPerm, lazy='subquery',backref=db.backref('permisos', lazy='dynamic'))

    def __init__(self, nombre='', apellidos='', id_organizacion=0):
        self.nombre = nombre
        self.apellidos = apellidos


    def get_usuario(self, id):
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        return usuario


    def get_ult_usuario(self):
        usuarios = Usuario.query.all()

        numOrg = len(usuarios)
        usuario = usuarios[numOrg - 1]

        return usuario


    def post_usuario(self):
        db.session.add(self)
        db.session.commit()


    def put_usuario(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        db.session.commit()

    def put_usuario_permisos(self, permiso):
        self.permisos.append(permiso)
        db.session.commit()

    def delete_usuario(self):
        db.session.delete(self)
        db.session.commit()

    def existe_usuario_permiso(self, id_permiso):
        for permiso in self.permisos:
            if(permiso.id_permiso==id_permiso):

                return True
        return False

    def delete_usuario_permiso(self, permiso):
        self.permisos.remove(permiso)
        db.session.commit()

    def get_permiso_usuarios(self, peticion_id):

        ids = db.session.query(UsuPerm).filter_by(id_permiso=peticion_id)
        usuarios=[]

        for id in ids:
            usuarios.append(Usuario().get_organizacion(id.usuario))

        return usuarios


#API Usuario
@app.route('/api/v1.0/usuarios/', methods=['GET'])
def muestraUsuarios():
    usuarios = []

    for usuario in Usuario.query.all():
        usuarios.append({
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
        })

    return json.dumps(usuarios, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['GET'])
def muestraUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)

@app.route('/api/v1.0/usuarios/', methods=['POST'])
def insertaUsuario():
    value = request.json

    nombre = value["nombre"]
    apellidos = value["apellidos"]

    usuarioIn = Usuario(nombre, apellidos)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos})


@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['PUT'])
def actualizaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json
        nombre = value["nombre"]
        apellidos = value["apellidos"]

        usuario = Usuario().get_usuario(usuario_id)

        usuario.put_usuario(nombre, apellidos)

        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
      abort(404)


@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['DELETE'])
def eliminaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if (usuario):
        usuario.delete_usuario()
        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)


#API Usuario-Permiso
@app.route('/api/v1.0/usuarios/<int:usuario_id>/permisos/', methods=['GET'])
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

@app.route('/api/v1.0/usuarios/<int:usuario_id>/permisos/<int:permiso_id>/', methods=['GET'])
def muestraUsuarioPerm(usuario_id, permiso_id):
    usuario = Usuario().get_usuario(usuario_id)

    if (usuario):
        if(usuario.existe_usuario_permiso(permiso_id)):
            permiso = Permiso().get_permiso(permiso_id)
            return jsonify({"id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion" : permiso.id_estacion})
        else:
            abort(403)
    else:
        abort(404)


@app.route('/api/v1.0/usuarios/<int:usuario_id>/permisos/', methods=['POST'])
def insertaUsuarioPerm(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json

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


@app.route('/api/v1.0/usuarios/<int:usuario_id>/permisos/<int:permiso_id>/', methods=['PUT'])
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

@app.route('/api/v1.0/usuarios/<int:usuario_id>/permisos/<int:permiso_id>/', methods=['DELETE'])
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

# API Permiso-Usuario
@app.route('/api/v1.0/permisos/<int:permiso_id>/usuarios/', methods=['GET'])
def muestraPermisosUsu(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if(permiso):
        usuarios = Usuario().get_peticion_usuarios(permiso_id)
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


