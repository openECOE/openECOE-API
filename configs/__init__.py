#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

import os
from ast import literal_eval

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))




# Default configuration
os.environ.setdefault("OPENECOE_SECRET", "111111111111111111111")
os.environ.setdefault("OPENECOE_DB_HOST", "localhost")
os.environ.setdefault("OPENECOE_DB_PORT", "3306")
os.environ.setdefault("OPENECOE_DB_USER", "openecoe")
os.environ.setdefault("OPENECOE_DB_PASSWORD", "openecoe_pass")
os.environ.setdefault("OPENECOE_DB_NAME", "openECOE")
os.environ.setdefault("OPENECOE_DB_PARAMS", "")

os.environ.setdefault("OPENECOE_REDIS_HOST", "redis")
os.environ.setdefault("OPENECOE_REDIS_PORT", "6379")
os.environ.setdefault("OPENECOE_REDIS_DB", "0")

os.environ.setdefault("SERVER_NAME", "localhost")

# Debug configuration
os.environ.setdefault("BCRYPT_LOG_ROUNDS", "10")
os.environ.setdefault("DEBUG", "False")
os.environ.setdefault("TESTING", "False")
os.environ.setdefault("LOG_TO_STDOUT", "False")
os.environ.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", "False")
os.environ.setdefault("API_AUTH", "True")
os.environ.setdefault("SQLALCHEMY_ECHO", "False")

envpath = os.path.join(basedir, ".env")

load_dotenv(dotenv_path=envpath, override=True)


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get("OPENECOE_SECRET")
    BCRYPT_LOG_ROUNDS = literal_eval(os.environ.get("BCRYPT_LOG_ROUNDS"))
    DEBUG = literal_eval(os.environ.get("DEBUG"))
    TESTING = literal_eval(os.environ.get("TESTING"))
    LOG_TO_STDOUT = literal_eval(os.environ.get("LOG_TO_STDOUT"))
    API_AUTH = literal_eval(os.environ.get("API_AUTH"))
    CORS_EXPOSE_HEADERS = "x-total-count"
    EXPORT_FILE_TYPES = ["csv", "tsv", "csvz", "tsvz", "xls", "xlsx", "xlsm", "ods"]
    DEFAULT_EXPORT_FILE_TYPE = "csv"
    DEFAULT_ARCHIVE_ROUTE = "archive"
    DEFAULT_TEMPLATE_ROUTE = "template"
    CHRONO_ROUTE = "http://localhost:5001"
    
    
    """Potion configuration."""
    POTION_DEFAULT_PER_PAGE = 50
    POTION_MAX_PER_PAGE = 200
    
    """SQLAlchemy config"""
    OPENECOE_DB_HOST = os.environ.get("OPENECOE_DB_HOST")
    OPENECOE_DB_PORT = os.environ.get("OPENECOE_DB_PORT")
    OPENECOE_DB_USER = os.environ.get("OPENECOE_DB_USER")
    OPENECOE_DB_PASSWORD = os.environ.get("OPENECOE_DB_PASSWORD")
    OPENECOE_DB_NAME = os.environ.get("OPENECOE_DB_NAME")
    OPENECOE_DB_PARAMS = os.environ.get("OPENECOE_DB_PARAMS")
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{OPENECOE_DB_USER}:{OPENECOE_DB_PASSWORD}@{OPENECOE_DB_HOST}:{OPENECOE_DB_PORT}/{OPENECOE_DB_NAME}{OPENECOE_DB_PARAMS}"
    SQLALCHEMY_TRACK_MODIFICATIONS = literal_eval(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    )
    SQLALCHEMY_ECHO = literal_eval(
        os.environ.get("SQLALCHEMY_ECHO")
    )

    """Redis configuration"""
    OPENECOE_REDIS_HOST = os.environ.get("OPENECOE_REDIS_HOST")
    OPENECOE_REDIS_PORT = os.environ.get("OPENECOE_REDIS_PORT")
    OPENECOE_REDIS_DB = os.environ.get("OPENECOE_REDIS_DB") 
    
    RQ_REDIS_URL = f"redis://{OPENECOE_REDIS_HOST}:{OPENECOE_REDIS_PORT}/{OPENECOE_REDIS_DB}"
    RQ_DEFAULT_QUEUE = "openecoe_jobs"
    RQ_QUEUES = ["openecoe_jobs"]


class TestConfig(BaseConfig):
    """Test configuration"""

    TESTING = True
    DEBUG = True
    API_AUTH = True
    SQLALCHEMY_DATABASE_URI = "%s_test" % os.environ.get("SQLALCHEMY_DATABASE_URI")
