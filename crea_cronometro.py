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

