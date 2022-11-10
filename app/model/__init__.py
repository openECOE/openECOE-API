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

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import flask_app

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

db.init_app(flask_app)
migrate.init_app(flask_app, db)
bcrypt.init_app(flask_app)


from app.model.Area import Area
from app.model.ECOE import ECOE
from app.model.Event import Event
from app.model.Job import Job
from app.model.Organization import Organization
from app.model.Planner import Planner
from app.model.Question import Block, Question
from app.model.Round import Round
from app.model.Schedule import Schedule
from app.model.Shift import Shift
from app.model.Stage import Stage
from app.model.Station import Station
from app.model.Student import Answer, Student
from app.model.User import User
