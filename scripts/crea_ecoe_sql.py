import mysql.connector
import json
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta

# Credenciales 
USER = "ecoe@umh.es"
PASSWORD = "Kui0chee"
ORGANIZATION = 'UV'
NAME_ECOE = 'ECOE_2023'
DURATION = 7
"""
# ---------------------------
# 0. Crear organización
# ---------------------------
url_organizacion = "http://localhost:5000/backend/api/v1/organizations"

payload_organization = {
    "name": ORGANIZATION
}

response_org = requests.post(
    url_organizacion,
    json=payload_organization,
    auth=HTTPBasicAuth(USER, PASSWORD)
)

if response_org.status_code in (200, 201):
    data = response_org.json()
    uri_org = data.get("$uri")  # Ej: "/backend/api/v1/organizations/2"
    print("✔ ORGANIZACION creada:", uri_org)
    org_id = int(uri_org.split("/")[-1])
    print("ORGANIZACION_ID:",org_id)  # 2
     
else:
    print("❌ Error al crear ORGANIZACION:", response_org.text)
    exit()

# ---------------------------
# 1. Crear el ECOE
# ---------------------------
url_ecoes = "http://localhost:5000/backend/api/v1/ecoes"

payload_ecoe = {
    "name": NAME_ECOE,
    "organization": {        
        "$ref": f"/backend/api/v1/organizations/{org_id}"
    }
}

response = requests.post(
    url_ecoes,
    json=payload_ecoe,
    auth=HTTPBasicAuth(USER, PASSWORD)
)

if response.status_code in (200, 201):
    data = response.json()
    uri_ecoe = data.get("$uri")  # Ej: "/backend/api/v1/ecoes/7"
    print("✔ ECOE creada:", uri_ecoe)     
    ecoe_id = int(uri_ecoe.split("/")[-1])
    print("ECOE_ID:",ecoe_id)  # 2
else:
    print("❌ Error al crear ECOE:", response.text)
    exit()



# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)


if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
        else:
            print("No se encontró el ecoe con ese nombre")


# ---------------------------
# 2. Crear Área usando el ECOE creado
# ---------------------------
url_areas = "http://localhost:5000/backend/api/v1/areas"
uri_ecoe = f"/backend/api/v1/ecoes/{ecoe_id}"
# Lista de áreas a crear
areas = [
    {"code": "A1", "name": "Área 1", "weith": 10},
    {"code": "A2", "name": "Área 2", "weith": 20},
    {"code": "A3", "name": "Área 3", "weith": 15},
    # ... agrega hasta 10 o más
]

# Iteramos y hacemos POST por cada área
for area in areas:
    payload_area = {
        "code": area["code"],
        "ecoe": {"$ref": uri_ecoe},
        "name": area["name"],
        "weith": area["weith"]
    }

    response = requests.post(
        url_areas,
        json=payload_area,
        auth=HTTPBasicAuth(USER, PASSWORD)
    )

    if response.status_code in (200, 201):
        data = response.json()
        uri_area = data.get("$uri")
        print(f"✔ Área creada correctamente: {uri_area}")
    else:
        print(f"❌ Error al crear el área {area['name']}: {response.text}")
       

    conn.close()

else:

    print("No podemos conectar con DB")


# ---------------------------
# 3. Crear ESTACIONES usando el ECOE creado
# ---------------------------
# Lista de estaciones a crear
url_estaciones = "http://localhost:5000/backend/api/v1/stations"
uri_ecoe = f"/backend/api/v1/ecoes/{ecoe_id}"

estaciones = [
    {"name": "Estación 1", "order": 1},
    {"name": "Estación 2", "order": 2},
    {"name": "Estación 3", "order": 3},
    # ... hasta 10
]

# Iteramos y hacemos POST por cada estación
for estacion in estaciones:
    payload_estacion = {
        "name": estacion["name"],
        "order": estacion["order"],
        "ecoe": {"$ref": uri_ecoe}
    }

    response = requests.post(
        url_estaciones,
        json=payload_estacion,
        auth=HTTPBasicAuth(USER, PASSWORD)
    )

    if response.status_code in (200, 201):
        data = response.json()
        uri_station = data.get("$uri")
        print(f"✔ Estación creada correctamente: {uri_station}")
    else:
        print(f"❌ Error al crear la estación {estacion['name']}: {response.text}")

    conn.close()

# ---------------------------
# 4. Crear Preguntas para la Estación 
# ---------------------------
# 4.1 Crear Bloque de Preguntas
# ---------------------------
url_bloque = "http://localhost:5000/backend/api/v1/blocks"
# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
        else:
            print("No se encontró el ecoe con ese nombre")

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query                
        query = "SELECT id FROM openECOE_dev.station WHERE id_ecoe = %s"
        cursor.execute(query, (ecoe_id,))
        results = cursor.fetchall()
        for row in results:
            print("ID_STATION:", row[0])
            uri_station = f"/backend/api/v1/stations/{row[0]}"
            print("uri_station:", uri_station)
            payload_bloque = {
                "name": "BLOQUE1", 
                "station": {"$ref": uri_station},        
                "order": 1
            }
            response4 = requests.post(
                url_bloque,
                json=payload_bloque,
                auth=HTTPBasicAuth(USER, PASSWORD)
            )
            if response4.status_code in (200, 201):
                data = response4.json()
                uri_bloque = data.get("$uri")  # Ej: "/backend/api/v1/blocks/194"
                print("✔ Bloque creado correctamente", uri_bloque)    
                print(response4.json())
            else:
                print("❌ Error al crear el Bloque:", response4.text)
                exit()

# ---------------------------
# 4.1 Crear Preguntas
# ---------------------------

url_questions = "http://localhost:5000/backend/api/v1/questions"
# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
        else:
            print("No se encontró el ecoe con ese nombre")

if conn and conn.is_connected():
    with conn.cursor() as cursor:
        query = '''
        SELECT s.id AS station_id, s.name AS station_name, 
               a.id AS area_id, a.name AS area_name
        FROM openECOE_dev.station s 
        CROSS JOIN openECOE_dev.area a 
        WHERE s.id_ecoe = %s AND a.id_ecoe = %s
        '''
        cursor.execute(query, (ecoe_id, ecoe_id))
        results = cursor.fetchall()
        
        for row in results:
            station_id, station_name, area_id, area_name = row
            print(f"\n🟦 Estación {station_name} ({station_id}) | Área {area_name} ({area_id})")

            # 📌 1) OBTENER EL BLOQUE DE ESA ESTACIÓN
            query_block = "SELECT id FROM openECOE_dev.block WHERE id_station = %s LIMIT 1"
            cursor.execute(query_block, (station_id,))
            block_result = cursor.fetchone()
            
            if not block_result:
                print(f"⚠ No existe bloque para la estación {station_name}. Saltando...")
                continue

            block_id = block_result[0]
            uri_bloque = f"/backend/api/v1/blocks/{block_id}"
            print(f"📌 Bloque asociado → {uri_bloque}")

            # 🔥 Tus preguntas
            preguntas = [
                {"description": "Pregunta 1", "options": [{"id_option": 1,"points": 1,"label": "Sí","order": 0}]},
                {"description": "Pregunta 2", "options": [{"id_option": 1,"points": 0,"label": "No","order": 0}]},
                {"description": "Pregunta 3", "options": [
                    {"id_option": 1,"points": 2,"label": "Correcto","order": 0},
                    {"id_option": 2,"points": 0,"label": "Incorrecto","order": 1}
                ]}
            ]

            # 📝 2) Crear preguntas ligadas a ese bloque
            for orden, p in enumerate(preguntas, start=1):
                question_schema = {
                    "type": "radio",
                    "reference": f"REF-{station_id}-{area_id}-{orden}",
                    "description": p["description"],
                    "options": p["options"]
                }

                payload = {
                    "area": {"$ref": f"/backend/api/v1/areas/{area_id}"},
                    "station": {"$ref": f"/backend/api/v1/stations/{station_id}"},
                    "order": orden,
                    "block": {"$ref": uri_bloque},   # 🔥 Ya conectado al bloque correcto
                    "question_schema": json.dumps(question_schema),
                    "max_points": max(opt["points"] for opt in p["options"])
                }

                response = requests.post(url_questions,json=payload,auth=HTTPBasicAuth(USER, PASSWORD))

                if response.status_code in (200, 201):
                    print("✔ Pregunta creada:", response.json().get("$uri"))
                else:
                    print("❌ Error:", response.text)

# ---------------------------
# 5. Crear Cronometro
# 5.1 Añadir Fase / Stages
# ---------------------------
url_stages = "http://localhost:5000/backend/api/v1/stages"
# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
        else:
            print("No se encontró el ecoe con ese nombre")
payload_stage = {
    "duration": DURATION * 60,
    "name": 'Fase1',
    "ecoe": {
    "$ref": f"/backend/api/v1/ecoes/{ecoe_id}"
    },
    "order": 1
}

response = requests.post(
    url_stages,
    json=payload_stage,
    auth=HTTPBasicAuth(USER, PASSWORD)
)

if response.status_code in (200, 201):
    data = response.json()
    uri_stage = data.get("$uri")  # Ej: "/backend/api/v1/stages/8"
    print("✔ STAGE creado:", uri_stage)
    stage_id = int(uri_stage.split("/")[-1])
    print("STAGE_ID:",stage_id)  # 2

else:
    print("❌ Error al crear STAGE:", response.text)
    exit()
# ---------------------------
# 5.2 creamos SCHEDULES
# ---------------------------
url_schedule = "http://localhost:5000/backend/api/v1/schedules"
payload_schedule = {
    "stage": {
        "$ref": f"/backend/api/v1/stages/{stage_id}"    
    },    
    "ecoe": {
    "$ref": f"/backend/api/v1/ecoes/{ecoe_id}"
    }   
}
response = requests.post(
    url_schedule,
    json=payload_schedule,
    auth=HTTPBasicAuth(USER, PASSWORD)
)
if response.status_code in (200, 201):
    data = response.json()
    uri_schedule = data.get("$uri")  # Ej: "/backend/api/v1/stages/8"
    print("✔ SCHEDULE creado:", uri_schedule)
    schedule_id = int(uri_schedule.split("/")[-1])
    print("STAGE_ID:",schedule_id)  
else:
    print("❌ Error al crear SCHEDULE:", response.text)
    exit()

# SELECT * FROM openECOE_dev.schedule where id_ecoe = 38
# ---------------------------
# 5.2 Create EVENTS (2 enventos)
# ---------------------------
url_event = "http://localhost:5000/backend/api/v1/events"

# Lista de eventos a crear
eventos = [
    {
        "schedule": {"$ref": f"/backend/api/v1/schedules/{schedule_id}"},
        "time": 0,
        "is_countdown": False,
        "sound": None,
        "text": "Start"
    },
    {
        "schedule": {"$ref": f"/backend/api/v1/schedules/{schedule_id}"},
        "time": 420,
        "is_countdown": False,
        "sound": None,
        "text": "End"
    }
]

# Bucle para crear todos los eventos en la lista
for i, payload in enumerate(eventos, start=1):

    response = requests.post(
        url_event,
        json=payload,
        auth=HTTPBasicAuth(USER, PASSWORD)
    )

    if response.status_code in (200, 201):
        uri_event = response.json().get("$uri")
        print(f"✔ EVENT {i} creado:", uri_event)
    else:
        print(f"❌ Error creando EVENT {i}:", response.text)
        exit()
# ---------------------------
# 6. Create STUDENTS
# ---------------------------
url_student = "http://localhost:5000/backend/api/v1/students"

# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
            uri_ecoe = f"/backend/api/v1/ecoes/{ecoe_id}"
        else:
            print("No se encontró el ecoe con ese nombre")

students = [
    {"dni": "A001", "name": "Alumno1", "surnames": "Apellidos1", "planner": 'null'},
    {"dni": "A002", "name": "Alumno2", "surnames": "Apellidos2", "planner": 'null'},
    {"dni": "A002", "name": "Alumno3", "surnames": "Apellidos3", "planner": 'null'},
    # ... hasta 10
]

# Iteramos y hacemos POST por cada estudiante
for student in students:
    
    payload_student = {
        "ecoe": {"$ref": uri_ecoe},
        "dni": student["dni"],
        "name": student["name"],
        "surnames": student["surnames"],
        "planner": None         
    }

    response = requests.post(
        url_student,
        json=payload_student,
        auth=HTTPBasicAuth(USER, PASSWORD)
    )

    if response.status_code in (200, 201):
        data = response.json()
        uri_station = data.get("$uri")
        print(f"✔ EStudiante creado correctamente: {uri_station}")
    else:
        print(f"❌ Error al crear al estudiante {student['name']}: {response.text}")

    conn.close()

# ---------------------------
# 7. Create planner id_shift, id_round
# 7.1 Crea Ronda / Round = Una Única ronda
# ---------------------------
url_round = "http://localhost:5000/backend/api/v1/rounds"
# {"ecoe":10,"round_code":"Ronda1","description":"Ronda1"}
# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)
            uri_ecoe = f"/backend/api/v1/ecoes/{ecoe_id}"
        else:
            print("No se encontró el ecoe con ese nombre")

payload_round = {
        "ecoe": {"$ref": uri_ecoe},
        "round_code": "Ronda1",
        "description": "Ronda1"        
}
response = requests.post(
    url_round,
    json=payload_round,
    auth=HTTPBasicAuth(USER, PASSWORD)
)

if response.status_code in (200, 201):
    data = response.json()
    uri_round = data.get("$uri")
    print(f"✔ Ronda creada correctamente: {uri_round}")
else:
    print(f"❌ Error al crear Ronda {uri_round}: {response.text}")

# ---------------------------
# 7.2 Crea turno / shift (varios turnos)
# ---------------------------

url_shift = "http://localhost:5000/backend/api/v1/shifts"
#{"ecoe":10,"shift_code":"t3","time_start":{"$date":1719411480000}}
# 7 min X 12 alumnos = 84 minutos
# ---------------------------
# datetime.datetime(AÑO, MES, DÍA, HORA, MINUTO)
# Fecha y hora actuales
hoy = datetime.now()

# Mañana a las 08:00
manana_8 = (hoy + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)

timestamp_ms = int(manana_8.timestamp() * 1000)

# Lista de turnos
turnos = [    
    {"ecoe": ecoe_id, "shift_code": "t1", "time_start": {"$date": 0}},
    {"ecoe": ecoe_id, "shift_code": "t2", "time_start": {"$date": 0}},
    {"ecoe": ecoe_id, "shift_code": "t3", "time_start": {"$date": 0}},
    {"ecoe": ecoe_id, "shift_code": "t4", "time_start": {"$date": 0}},
]

# Intervalo entre turnos en minutos
intervalo = 84

# Asignar el timestamp en ms dentro del diccionario
for i, turno in enumerate(turnos):
    tiempo_turno = manana_8 + timedelta(minutes=i*intervalo)
    # 🔹 Aquí se actualiza directamente el diccionario
    turno["time_start"]["$date"] = int(tiempo_turno.timestamp() * 1000)

# Iteramos y hacemos POST por cada turno
for turno in turnos:
    
    payload_turno = {
        "ecoe": turno["ecoe"],
        "shift_code": turno["shift_code"],
        "time_start": turno["time_start"]        
    }

    response = requests.post(
        url_shift,
        json=payload_turno,
        auth=HTTPBasicAuth(USER, PASSWORD)
    )

    if response.status_code in (200, 201):
        data = response.json()
        uri_turno = data.get("$uri")
        print(f"✔ TURNO creado correctamente: {uri_round}")
    else:
        print(f"❌ Error al crear TURNO {turno['shift_code']}: {response.text}")

    conn.close()
"""
# ---------------------------
# Asignar Alunos a los turnos creados previamente
# ---------------------------
# SELECT * FROM openECOE_dev.student WHERE id_ecoe = 38;
url_planner = "http://localhost:5000/backend/api/v1/students/717"
#PATCH
#{"planner":{"$ref":"/backend/api/v1/planners/18"},"planner_order":1}
#{"planner":{"$ref":"/backend/api/v1/planners/20"},"planner_order":1}
# Conexión a DB
conn = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev'
)

if conn and conn.is_connected():
    print("Conectado correctamente!")
    # Creamos un cursor
    with conn.cursor() as cursor:
        # Execute a query        
        query = "SELECT id FROM openECOE_dev.ecoe WHERE name = %s"
        cursor.execute(query, (NAME_ECOE,))
        result = cursor.fetchone() 

        if result:
            ecoe_id = result[0]
            print("ID encontrado:", ecoe_id)            
        else:
            print("No se encontró el ecoe con ese nombre")
      
        query = "SELECT id FROM openECOE_dev.student WHERE id_ecoe = %s"         
        cursor.execute(query, (ecoe_id,))                
        rows = cursor.fetchall()
        
        student_ids = [row[0] for row in rows]
        # ID's studiantes
        print(student_ids)
        cursor.execute("SELECT id FROM openECOE_dev.round WHERE id_ecoe = %s", (ecoe_id,))    
        row  = cursor.fetchone()
        if row:
            id_round = row[0]  
        else:
            raise ValueError("No se encontró la ronda")
        print(id_round)
        cursor.execute("SELECT id FROM openECOE_dev.shift WHERE id_ecoe = %s", (ecoe_id,))    
        rows = cursor.fetchall()
        shift_ids = [row[0] for row in rows]
        print(shift_ids)

        planners_created = []  # para guardar id de planner insertados

        # 1️⃣ Crear un planner por cada shift
        for shift_id in shift_ids:
            cursor.execute(
                "INSERT INTO openECOE_dev.planner (id_shift, id_round) VALUES (%s, %s)",
                (shift_id, id_round)
            )
            planner_id = cursor.lastrowid
            planners_created.append(planner_id)
        # Asignación Alumnos a los turnos
        # Ejemplo: round-robin
        for i, student_id in enumerate(student_ids):
            planner_index = i % len(planners_created)  # ciclo entre los planners
            planner_id = planners_created[planner_index]
            planner_order = (i // len(planners_created)) + 1  # orden dentro del planner

            cursor.execute(
                "UPDATE openECOE_dev.student SET id_planner = %s, planner_order = %s WHERE id = %s",
                (planner_id, planner_order, student_id)
            )

        conn.commit()
        cursor.close()
        conn.close()

        
            

"""
else:
    print("No podemos conectar con DB")
"""