import os

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)

app.config.from_object(app_settings)

bcrypt = Bcrypt(app)

import api