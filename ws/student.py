from ws import *
from model import ECOE, Student, Round, Shift, Day

def existEcoeStudent(student, ecoe_id):
    if(student):
        if(student.id_ecoe == ecoe_id):
            return True
        else:
            return False
    else:
        return False

#Relacion ECOE-Alumno
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/', methods=['GET'])
def getStudents(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        students = []
        for student in ecoe.students:
            students.append({
                "id_student" : student.id_student,
                "name" : student.name,
                "DNI" : student.dni
        })

        return json.dumps(students, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<student_id>/', methods=['GET'])
def getStudent(ecoe_id, student_id):
    student = Student().get_student(student_id)

    if(existEcoeStudent(student, ecoe_id) == False):
        abort(404)

    return jsonify({"id_student": student.id_student, "name": student.name, "dni" : student.dni})



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/', methods=['POST'])
def postStudent(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "name" in request.json) or (not "dni" in request.json)):
            abort(400)

        name = value["name"]
        dni = value["dni"]

        student = Student(name, dni, ecoe_id)
        student.post_student()

        student = Student().get_last_student()

        return jsonify({"id_student": student.id_student, "name": student.name, "dni": student.dni})
    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<student_id>/', methods=['PUT'])
def putStudent(ecoe_id, student_id):
    student = Student().get_student(student_id)
    if (existEcoeStudent(student, ecoe_id) == False):
        abort(404)

    value = request.json

    if ((not request.json) or (not "name" in request.json)  or (not "dni" in request.json) or (not "id_ecoe" in request.json)):
        abort(400)

    name = value["name"]
    dni = value["dni"]
    id_ecoe = value["id_ecoe"]

    student.put_student(name, dni, id_ecoe)

    return jsonify({"id_student": student.id_student, "name": student.name, "dni": student.dni})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/student/<student_id>/', methods=['DELETE'])
def delStudent(ecoe_id, student_id):
    student = Student().get_student(student_id)

    if (existEcoeStudent(student, ecoe_id) == False):
        abort(404)

    student.delete_student()
    return jsonify({"id_student": student.id_student, "name": student.name, "dni": student.dni})


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

        alumno = Student().get_student(alumno_id)
        return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})

    else:
        abort(404)




@app.route('/api/v1.0/wheel/<int:rueda_id>/student/<int:alumno_id>/', methods=['PUT'])
def modificaAlumnoRueda(rueda_id, alumno_id):
    rueda = Round().get_rueda(rueda_id)
    if (rueda==False):
        abort(404)

    alumno = Student().get_student(alumno_id)
    if(alumno == False):
        abort(404)

    turno = Shift().get_turno(rueda.id_turno)
    dia = Day().get_day(turno.id_dia)

    if(dia.id_ecoe != alumno.id_ecoe):
        abort(404)

    alumno.put_student_id_round(rueda_id)

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})


@app.route('/api/v1.0/wheel/<int:rueda_id>/student/<int:alumno_id>/', methods=['DELETE'])
def eliminaAlumnoRueda(rueda_id, alumno_id):
    rueda = Round().get_rueda(rueda_id)
    if (rueda == False):
        abort(404)

    if (rueda.existe_rueda_alumno(alumno_id) == False):
        abort(404)

    alumno = Student().get_student(alumno_id)
    alumno.delete_student_id_round()

    return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
