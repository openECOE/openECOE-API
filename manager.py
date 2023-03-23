from flask import Flask
from flask_script import Manager
from openecoe-api import app as api
from openecoe-chrono import app as chrono
import psutil

manager = Manager()

app = Flask(__name__)

@manager.command
def runserver():   
    api.run(port=5000, debug=True)
    chrono.run(port=5001, debug=True)
    
@manager.command
def stopserver():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in proc.info['name'] and '5000' in proc.info['cmdline']:
            proc.kill()
            print('API service stopped.')
        elif 'python' in proc.info['name'] and '5001' in proc.info['cmdline']:
            proc.kill()
            print('Chrono service stopped.')