from ws import *
from model import ECOE, Student, Round, Shift, Day

def existEcoeStudent(alumno, ecoe_id):
    if(alumno):
        if(alumno.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False

#Relacion ECOE-Alumno
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/', methods=['GET'])
def obtenAlumnos(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        alumnos = []
        for alumno in ecoe.alumnos:
            alumnos.append({
                "id_alumno" : alumno.id_alumno,
                "nombre" : alumno.nombre,
                "DNI" : alumno.dni
        })

        return json.dumps(alumnos, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<int:alumno_id>/', methods=['GET'])
def obtenAlumno(ecoe_id, alumno_id):
    alumno = Student().get_alumno(alumno_id)

    if(existEcoeStudent(alumno, ecoe_id) == False):
        abort(404)

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni" : alumno.dni})



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/', methods=['POST'])
def insertaAlumno(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "dni" in request.json)):
            abort(400)

        nombre = value["nombre"]
        dni = value["dni"]

        alumnoIn = Student(nombre, dni, ecoe_id)
        alumnoIn.post_alumno()

        alumno = Student().get_ult_alumno()

        return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<int:alumno_id>/', methods=['PUT'])
def modificaAlumno(ecoe_id, alumno_id):
    alumno = Student().get_alumno(alumno_id)
    if (existEcoeStudent(alumno, ecoe_id) == False):
        abort(404)

    value = request.json

    if ((not request.json) or (not "nombre" in request.json)  or (not "dni" in request.json) or (not "id_ecoe" in request.json)):
        abort(400)

    nombre = value["nombre"]
    dni = value["dni"]
    id_ecoe = value["id_ecoe"]

    alumno.put_alumno(nombre, dni, id_ecoe)

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<int:alumno_id>/', methods=['DELETE'])
def eliminaAlumno(ecoe_id, alumno_id):
    alumno = Student().get_alumno(alumno_id)

    if (existEcoeStudent(alumno, ecoe_id) == False):
        abort(404)

    alumno.delete_alumno()
    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})


#Rutas Rueda-Alumno
# RUTAS DE TURNO
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/<int:dia_id>//round/<int:rueda_id>/student/', methods=['GET'])
def muestraAlumnosRueda(rueda_id):
    rueda = Round().get_rueda(rueda_id)

    if (rueda):
        alumnos = []

        for alumno in rueda.alumnos:
            alumnos.append({
                "id_alumno": alumno.id_alumno,
                "nombre": alumno.nombre,
                "dni": alumno.dni
            })

        return json.dumps(alumnos, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


# RUTAS DE Rueda-Alumno
@app.route('/api/v1.0/wheel/<int:rueda_id>/student/<int:alumno_id>/', methods=['GET'])
def muestraAlumnoRueda(rueda_id, alumno_id):
    rueda = Round().get_rueda(rueda_id)

    if (rueda):
        if(rueda.existe_rueda_alumno(alumno_id)==False):
            abort(404)

        alumno = Student().get_alumno(alumno_id)
        return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})

    else:
        abort(404)




@app.route('/api/v1.0/wheel/<int:rueda_id>/student/<int:alumno_id>/', methods=['PUT'])
def modificaAlumnoRueda(rueda_id, alumno_id):
    rueda = Round().get_rueda(rueda_id)
    if (rueda==False):
        abort(404)

    alumno = Student().get_alumno(alumno_id)
    if(alumno == False):
        abort(404)

    turno = Shift().get_turno(rueda.id_turno)
    dia = Day().get_dia(turno.id_dia)

    if(dia.id_ecoe != alumno.id_ecoe):
        abort(404)

    alumno.put_alumno_id_rueda(rueda_id)

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})


@app.route('/api/v1.0/wheel/<int:rueda_id>/student/<int:alumno_id>/', methods=['DELETE'])
def eliminaAlumnoRueda(rueda_id, alumno_id):
    rueda = Round().get_rueda(rueda_id)
    if (rueda == False):
        abort(404)

    if (rueda.existe_rueda_alumno(alumno_id) == False):
        abort(404)

    alumno = Student().get_alumno(alumno_id)
    alumno.delete_alumno_id_rueda()

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
