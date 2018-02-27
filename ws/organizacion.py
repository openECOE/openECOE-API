from ws import *
from model import Organizacion, Usuario

#Rutas de Organizacion
@app.route('/api/v1.0/organization/', methods=['GET'])
def muestraOrganizaciones():
    organizaciones = []

    for organizacion in Organizacion.query.all():
        organizaciones.append({
            "id_organizacion": organizacion.id_organizacion,
            "nombre": organizacion.nombre,
        })

    return json.dumps(organizaciones, indent=1, ensure_ascii=False).encode('utf8')


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['GET'])
def muestraOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})

    else:
        abort(404)


@app.route('/api/v1.0/organization/', methods=['POST'])
def insertaOrganizacion():
    value = request.json

    if not request.json or not "nombre" in request.json:
        abort(400)

    nombre = value["nombre"]

    orgIn = Organizacion(nombre)
    orgIn.post_organizacion()

    org = Organizacion().get_ult_organizacion()
    return jsonify({"id": org.id_organizacion, "nombre": org.nombre})


@app.route('/api/v1.0/organization/<int:organizacion_id>/', methods=['PUT'])
def modificaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        value = request.json

        if not request.json or not "nombre" in request.json:
            abort(400)

        nombre = value["nombre"]



        organizacion.put_organizacion(nombre)

        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/organization/<int:organizacion_id>/', methods=['DELETE'])
def eliminaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        organizacion.delete_organizacion()
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})
    else:
        abort(404)



#Rutas de Usuarios-Organizacion
@app.route('/api/v1.0/user/<int:usuario_id>/organization/', methods=['GET'])
def muestraOrganizacionesUsu(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)
    if(usuario):
        organizaciones = Organizacion().get_usuario_organizaciones(usuario_id)
        estructura = []

        for organizacion in organizaciones:
            estructura.append({
                "id_organizacion": organizacion.id_organizacion,
                "nombre": organizacion.nombre,
            })

        return json.dumps(estructura, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)



