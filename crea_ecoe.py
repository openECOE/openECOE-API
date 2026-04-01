import requests
from requests.auth import HTTPBasicAuth
import json

# Organización Medicia
ID_ORGANIZATION = 2
# Credenciales 
USER = "ecoe@umh.es"
PASSWORD = "Kui0chee"
NAME_ECOE = 'ECOE'
NAME_AREA = 'A1'
CODE_AREA = 'A1'
WEITH_AREA = 100
NAME_STATION = 'Estacion1'

# ---------------------------
# 1. Crear el ECOE
# ---------------------------
url_ecoes = "http://localhost:5000/backend/api/v1/ecoes"

payload_ecoe = {
    "name": NAME_ECOE,
    "organization": {        
        "$ref": f"/backend/api/v1/organizations/{ID_ORGANIZATION}"
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
    print("✔ ECOE creado:", uri_ecoe)
else:
    print("❌ Error al crear ECOE:", response.text)
    exit()

# ---------------------------
# 2. Crear Área usando el ECOE creado
# ---------------------------
url_areas = "http://localhost:5000/backend/api/v1/areas"
payload_area = {
    "code": CODE_AREA,
    "ecoe": {"$ref": uri_ecoe},
    "name": NAME_AREA,
    "weith": WEITH_AREA
}

response2 = requests.post(
    url_areas,
    json=payload_area,
    auth=HTTPBasicAuth(USER, PASSWORD)
)

if response2.status_code in (200, 201):
    data = response2.json()
    uri_area = data.get("$uri")  # Ej: "/backend/api/v1/areas/68"
    print("✔ Área creada correctamente", uri_area)
    print(response2.json())
else:
    print("❌ Error al crear el área:", response2.text)
    exit()
# ---------------------------
# 3. Crear ESTACION usando el ECOE creado
# ---------------------------
url_estaciones = "http://localhost:5000/backend/api/v1/stations"
payload_estacion = {
    "name": NAME_STATION,
    "order": 1,
    "ecoe": {"$ref": uri_ecoe}
}
response3 = requests.post(
    url_estaciones,
    json=payload_estacion,
    auth=HTTPBasicAuth(USER, PASSWORD)
)
if response3.status_code in (200, 201):
    data = response3.json()
    uri_station = data.get("$uri")  # Ej: "/backend/api/v1/areas/68"
    print("✔ Estación creada correctamente", uri_station)    
    print(response3.json())
else:
    print("❌ Error al crear la estación:", response3.text)
    exit()

# ---------------------------
# 4. Crear Preguntas para la Estación 
# ---------------------------
# 4.1 Crear Bloque de Preguntas
# ---------------------------
url_bloque = "http://localhost:5000/backend/api/v1/blocks"

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
    uri_bloque = data.get("$uri")  # Ej: "/backend/api/v1/areas/68"
    print("✔ Bloque creado correctamente", uri_bloque)    
    print(response4.json())
else:
    print("❌ Error al crear el Bloque:", response4.text)
    exit()


# 4.1 Crear Preguntas
# ---------------------------
url_questions = "http://localhost:5000/backend/api/v1/questions"
question_schema = {
    "type": "radio",
    "reference": "Referencia1",
    "description": "texto de la pregunta",
    "options": [
        {"id_option": 1, "points": 1, "label": "Sí", "order": 0}
    ]
}
payload_questions = {
    "area": {"$ref": uri_area},
    "station": {"$ref": uri_station},
    "order": 1,
    "block": {"$ref": uri_bloque},
    "question_schema": json.dumps(question_schema),  
    "max_points": 1
}
response5 = requests.post(
    url_questions,
    json=payload_questions,
    auth=HTTPBasicAuth(USER, PASSWORD)
)
if response5.status_code in (200, 201):
    data = response5.json()
    uri_question = data.get("$uri")  # Ej: "/backend/api/v1/questions/850"
    print("✔ Question creada correctamente", uri_question)    
    print(response5.json())
else:
    print("❌ Error al crear la pregunta:", response5.text)
    exit() 