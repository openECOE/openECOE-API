from flask_potion import ModelResource
from flask_potion.routes import Relation

from model.Organization import Organization


class OrganizationResource(ModelResource):
    ecoes = Relation('ecoe')

    class Meta:
        model = Organization
        natural_key = ('name')
