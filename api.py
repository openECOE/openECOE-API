from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from Alarma import Alarma

alarma0 = Alarma(2,'aaaaaaaaaaa')

print (alarma0.getTiempo())

