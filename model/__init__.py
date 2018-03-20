from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from start import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .Organization import Organization
