from db import app

@app.route('/')
def holaMundo():
    return 'Hola Mundo'


app.run(port=5000, debug=True)