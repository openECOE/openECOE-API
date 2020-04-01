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
load_dotenv(os.path.join(basedir, '.env'))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BCRYPT_LOG_ROUNDS = literal_eval(os.environ.get('BCRYPT_LOG_ROUNDS'))
    DEBUG = literal_eval(os.environ.get('DEBUG'))
    TESTING = literal_eval(os.environ.get('TESTING'))
    LOG_TO_STDOUT = literal_eval(os.environ.get('LOG_TO_STDOUT'))
    SQLALCHEMY_TRACK_MODIFICATIONS = literal_eval(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
    API_AUTH = literal_eval(os.environ.get('API_AUTH'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CHRONO_ROUTE = os.environ.get('CHRONO_ROUTE')
    CORS_EXPOSE_HEADERS = 'x-total-count'
    EXPORT_FILE_TYPES = ['csv', 'tsv', 'csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods']
    DEFAULT_EXPORT_FILE_TYPE = 'csv'
    DEFAULT_ARCHIVE_ROUTE = 'archive'

    """Redis configuration"""
    RQ_DEFAULT_QUEUE = 'openecoe_jobs'
    RQ_QUEUES = ['openecoe_jobs']


class TestConfig(BaseConfig):
    """Test configuration"""
    TESTING = True
    DEBUG = True
    API_AUTH = True
    SQLALCHEMY_DATABASE_URI = "%s_test"%os.environ.get('SQLALCHEMY_DATABASE_URI')