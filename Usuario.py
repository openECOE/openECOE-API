from db import db

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))

    #TODO hacer que permisos sea relationship
    permisos = db.Column(db.Integer)

    def __init__(self, nombre='', apellidos='', permisos=[]):
        self.nombre = nombre
        self.apellidos = apellidos
        self.permisos = permisos

    def get_usuario(self, id):
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        return usuario

    def post_usuario(self):
        usuario = Usuario(nombre=self.nombre)
        usuario = Usuario(apellidos=self.apellidos)
        db.session.add(usuario)

        db.session.commit()
        return usuario

    #Edita nombre de Usuario
    def put_organizacionNombre(self, nombre):
        usuario = Usuario.query.filter_by(id_usuario=self.id_usuario).first()
        usuario.nombre = nombre
        db.session.commit()

        return usuario

    #Edita apellido de Usuario
    def put_organizacionApellidos(self, apellidos):
        usuario = Usuario.query.filter_by(id_usuario=self.id_usuario).first()
        usuario.apellidos = apellidos
        db.session.commit()

        return usuario

    def delete_usuario(self):
        usuario = Usuario.query.filter_by(id_usuario=self.id_usuario).first()

        db.session.delete(usuario)
        db.session.commit()

        return "OK"

    #TODO faltan los métodos relacionados con Permisos