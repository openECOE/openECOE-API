from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.QBlock import QBlock


class QblockResource(ModelResource):
    questions = Relation('question')

    class Meta:
        model = QBlock

    class Schema:
        station = fields.ToOne('station')

