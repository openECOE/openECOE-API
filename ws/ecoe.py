class EcoeResource(ModelResource):
    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('org')