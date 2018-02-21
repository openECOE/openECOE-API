from db import app
from db import db
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import abort, Response

import numpy as np
import json


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

    if ((not request.json) or (not "nombre" in request.json) or (not "apellidos" in request.json)):
        abort(400)

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

        if ((not request.json) or (not "nombre"  in request.json) or (not "apellidos" in request.json)):
            abort(400)

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


#Rutas de Organizacion-Usuarios
@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['GET'])
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


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['GET'])
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


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['POST'])
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



@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['PUT'])
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

@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['DELETE'])
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



# API Permiso-Usuario
#@app.route('/api/v1.0/permisos/<int:permiso_id>/usuarios/', methods=['GET'])
#def muestraPermisosUsu(permiso_id):
#    from Permiso import Permiso
#    permiso = Permiso().get_permiso(permiso_id)

 #   if(permiso):
 #       usuarios = Usuario().get_peticion_usuarios(permiso_id)
 #       estructura = []

 #       for usuario in usuarios:
 #           estructura.append({
  #              "id_usuario": usuario.id_usuario,
   #             "nombre": usuario.nombre,
   #             "apellidos": usuario.apellidos
    #        })

     #   return json.dumps(estructura, indent=1, ensure_ascii=False).encode('utf8')

    #else:
     #   abort(404)


