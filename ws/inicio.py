from db import app

from Organizacion import Organizacion


@app.route('/')
def holaMundo():
    return 'Hola Mundo'


app.run(port=5000, debug=True)