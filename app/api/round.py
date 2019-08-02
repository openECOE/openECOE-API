from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Round import Round
from app.api.ecoe import EcoePrincipalResource


class RoundResource(EcoePrincipalResource):
    planners = Relation('planners')

    class Meta:
        name = 'rounds'
        model = Round
        natural_key = ('ecoe', 'round_code')

    class Schema:
        ecoe = fields.ToOne('ecoes')
