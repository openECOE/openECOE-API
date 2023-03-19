from flask import Blueprint

bp =  Blueprint('chrono', __name__, template_folder='./templates')

bp.ecoes = []

from . import routes

"""
Reload configuration if exists on start
"""

from .classes import Manager

Manager.reload_status()