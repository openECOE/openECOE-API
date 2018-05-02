from flask_potion import ModelResource, fields
from app.model.QBlock import QBlock


class QblockResource(ModelResource):
    class Meta:
        model = QBlock

    class Schema:
        station = fields.ToOne('station')
        questions = fields.ToMany('question')
