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
id_ecoe= 35
duration = 7

# ---------------------------
# 1. Crear Cronometro
# 1.1 Añadir Fase / Stages
# ---------------------------
# {"duration":420,"name":"Fase1","ecoe":{"$ref":"/backend/api/v1/ecoes/35"},"order":0}
url_stages = "http://localhost:5000/backend/api/v1/stages"

payload_stage = {
    "duration": duration * 60,
    "name": 'Fase1',
    "ecoe": {
       "$ref": f"/backend/api/v1/ecoes/{id_ecoe}"
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
    uri_status = data.get("$uri")  # Ej: "/backend/api/v1/stages/8"
    print("✔ STAGE creado:", uri_status)
else:
    print("❌ Error al crear STAGE:", response.text)
    exit()
# ---------------------------
# creamos SCHEDULES
# ---------------------------
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

