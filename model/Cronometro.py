from db import db
from db import app
import numpy as np

from Estacion import Estacion

class Cronometro(db.Model):
    id_cronometro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tiempo_total = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estacion.id_estacion'))
    alarmas = db.relationship('Alarma', backref='alarmas', lazy='dynamic')

    def __init__(self, nombre='', tiempo_total=0, id_estacion=0):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion


        #self.alarmas = alarmas

    def get_cronometro(self, id):
        cronometro = Cronometro.query.filter_by(id_cronometro=id).first()
        return cronometro

    def get_ult_cronometro(self):
        cronometros = Cronometro.query.all()

        numCronometros = len(cronometros)
        cronometro = cronometros[numCronometros - 1]

        return cronometro


    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometro(self, nombre, tiempo_total, id_estacion):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion
        db.session.commit()


    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()

    def existe_cronometro_alarma(self, id_alarma):
        for alarma in self.alarmas:
            if(alarma.id_alarma==id_alarma):
                return True
        return False

#Relacion Estacion-Cronometro
@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['GET'])
def obtenCronometros(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        cronometros = []
        for cronometro in estacion.cronometros:
            cronometros.append({
                "id_cronometro": cronometro.id_cronometro,
                "nombre": cronometro.nombre,
                "tiempo_total": cronometro.tiempo_total
            })

        return json.dumps(cronometros, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['GET'])
def obtenCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total" : cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['POST'])
def insertaCronometro(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json)):
            abort(400)

        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometroIn = Cronometro(nombre, tiempo_total, estacion_id)
        cronometroIn.post_cronometro()

        cronometro = Cronometro().get_ult_cronometro()

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['PUT'])
def modificaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "tiempo_total" in request.json) or (not "id_estacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            tiempo_total = value["tiempo_total"]
            id_estacion = value["id_estacion"]

            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.put_cronometro(nombre, tiempo_total, id_estacion)

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.delete_cronometro()

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)


