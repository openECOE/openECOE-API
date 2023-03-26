import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from configs import BaseConfig

chrono_app = Flask(__name__)

chrono_app.ecoes = []
chrono_app.config.from_object(BaseConfig)

socketio = SocketIO(chrono_app,
                    async_mode= "eventlet",
                    logger = chrono_app.config["DEBUG"],
                    engineio_logger=chrono_app.config["DEBUG"],
                    cors_allowed_origins="*")
cors = CORS()

def create_chrono(config_class=BaseConfig):
    chrono_app.config.from_object(config_class)
    
    if not chrono_app.debug and not chrono_app.testing:
        if chrono_app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            chrono_app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/openecoe-chrono.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            chrono_app.logger.addHandler(file_handler)

        chrono_app.logger.setLevel(logging.INFO)
        chrono_app.logger.info("openECOE Chrono startup")
        
        cors.init_app(chrono_app)
        socketio.init_app(chrono_app)
        
    return chrono_app

from . import routes

"""
Reload configuration if exists on start
"""

from .classes import Manager

Manager.reload_status()
