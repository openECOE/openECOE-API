from ws import *
from model import Organization, User

#Rutas de Organizacion
@app.route('/api/v1.0/organization/', methods=['GET'])
def getOrganizations():
    organizations = []

    for organization in Organization.query.all():
        organizations.append({
            "id_organization": organization.id_organization,
            "name": organization.name,
        })

    return json.dumps(organizations, indent=1, ensure_ascii=False).encode('utf8')


@app.route('/api/v1.0/organization/<int:organization_id>/', methods=['GET'])
def getOrganization(organization_id):
    organization = Organization().get_organization(organization_id)

    if (organization):
        return jsonify({"id_organization": organization.id_organization, "name": organization.name})

    else:
        abort(404)


@app.route('/api/v1.0/organization/', methods=['POST'])
def postOrganization():
    value = request.json

    if not request.json or not "name" in request.json:
        abort(400)

    name = value["name"]

    orgIn = Organization(name)
    orgIn.post_organization()

    organization = Organization().get_last_organization()
    return jsonify({"id": organization.id_organization, "name": organization.name})


@app.route('/api/v1.0/organization/<organization_id>/', methods=['PUT'])
def putOrganization(organization_id):
    organization = Organization().get_organization(organization_id)

    if (organization):
        value = request.json

        if not request.json or not "name" in request.json:
            abort(400)

        name = value["name"]

        organization.put_organization(name)

        return jsonify({"id_organization": organization.id_organization, "name": organization.name})
    else:
        abort(404)


@app.route('/api/v1.0/organization/<organization_id>/', methods=['DELETE'])
def delOrganization(organization_id):
    organization = Organization().get_organization(organization_id)

    if (organization):
        organization.delete_organization()
        return jsonify({"id_organization": organization.id_organization, "name": organization.name})
    else:
        abort(404)



#Rutas de Usuarios-Organizacion
@app.route('/api/v1.0/user/<user_id>/organization/', methods=['GET'])
def getOrgUsu(user_id):
    user = User().get_user(user_id)
    if(user):
        organizations = Organization().get_user_organization(user_id)
        jsonOut = []

        for organization in organizations:
            jsonOut.append({
                "id_organization": organization.id_organization,
                "name": organization.name,
            })

        return json.dumps(jsonOut, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)



