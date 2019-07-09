from flask_potion import ModelResource, fields
from flask_potion.routes import Relation, ItemRoute
from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('areas')
    stations = Relation('stations')
    schedules = Relation('schedules')
    students = Relation('students')
    rounds = Relation('rounds')
    shifts = Relation('shifts')

    @ItemRoute.GET('/configuration')
    def configuration(self, ecoe) -> fields.String():
        return ecoe.configuration

    class Meta:
        name = 'ecoes'
        model = ECOE
        natural_key = 'name'

    class Schema:
        organization = fields.ToOne('organizations')


