from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import app

from Alarma import Alarma
from Area import Area

@app.route('/')
def holaMundo():
    return 'Hola Mundo'


@app.route('/<id>/', methods=['GET'])
def obtenArea(id):
    area = Area().get_area(id)
    return area.nombre

app.run(port=5000, debug=True)