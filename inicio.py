from db import app
from Organizacion import Organizacion
from Usuario import Usuario
from ECOE import ECOE
from Area import Area
from Alumno import Alumno
from Estacion import Estacion

@app.route('/')
def holaMundo():
    return 'Hola Mundo'


app.run(port=5000, debug=True)