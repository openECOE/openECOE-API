from ws import *
from model import User, Organization, Permission

#API Usuario
@app.route('/api/v1.0/user/', methods=['GET'])
def getUsers():
    users = []

    for user in User.query.all():
        users.append({
            "id_user": user.id_user,
            "name": user.name,
            "surname": user.surname
        })

    return json.dumps(users, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/user/<user_id>/', methods=['GET'])
def getUser(user_id):
    user = User().get_user(user_id)

    if(user):
        return jsonify({"id": user.id_user, "nombre": user.name, "apellidos": user.surname})
    else:
        abort(404)

@app.route('/api/v1.0/user/', methods=['POST'])
def insertaUsuario():
    value = request.json

    if ((not request.json) or (not "name" in request.json) or (not "surname" in request.json)):
        abort(400)

    name = value["name"]
    surname = value["surname"]

    userIn = User(name, surname)
    userIn.post_user()

    user = User().get_last_user()
    return jsonify({"id": user.id_user, "name": user.name, "surname" : user.surname})


@app.route('/api/v1.0/user/<user_id>/', methods=['PUT'])
def putUser(user_id):
    user = User().get_user(user_id)

    if(user):
        value = request.json

        if ((not request.json) or (not "name"  in request.json) or (not "surname" in request.json)):
            abort(400)

        name = value["name"]
        surname = value["surname"]

        user = User().get_user(user_id)
        user.put_user(name, surname)

        return jsonify({"id_usuario": user.id_user, "name": user.name, "surname": user.surname})
    else:
      abort(404)


@app.route('/api/v1.0/user/<user_id>/', methods=['DELETE'])
def delUSer(user_id):
    user = User().get_user(user_id)

    if (user):
        user.delete_user()
        return jsonify({"id_user": user.id_user, "name": user.name, "surname": user.surname})
    else:
        abort(404)


#Rutas de Organizacion-Usuarios
@app.route('/api/v1.0/organization/<organization_id>/user/', methods=['GET'])
def getUsersOrg(organization_id):
    organization = Organization().get_organization(organization_id)

    if (organization):
        users = []

        for user in organization.users:
            users.append({
                "id_user": user.id_user,
                "name": user.name,
                "surname": user.surname
            })

        return json.dumps(users, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/organization/<organization_id>/user/<user_id>/', methods=['GET'])
def muestraUsuarioOrg(organization_id, user_id):
    organization = Organization().get_organization(organization_id)

    if (organization):
        if(organization.exist_organization_user(user_id)):
            user = User().get_user(user_id)
            return jsonify({"id_user": user.id_user, "name": user.name, "name": user.name})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organization/<organization_id>/user/', methods=['POST'])
def postUserOrg(organization_id):
    organization = Organization().get_organization(organization_id)

    if(organization):
        value = request.json

        if ((not request.json) or (not "name"  in request.json) or (not "surname" in request.json)):
            abort(400)

        name = value["name"]
        surname = value["surname"]

        useroIn = User(name, surname)
        useroIn.post_user()

        user = User().get_last_user()
        organization.put_organization_user(user)

        return jsonify({"id_user": user.id_user, "name": user.name, "surname": user.surname})
    else:
        abort(404)



@app.route('/api/v1.0/organization/<organization_id>/user/<user_id>/', methods=['PUT'])
def putUserOrg(organization_id, user_id):
    organization = Organization().get_organization(organization_id)

    if(organization):
        user = User().get_user(user_id)
        if(user):
            if (organization.exist_organization_user(user_id) == False):
                organization.put_organization_user(user)
                return jsonify({"id_user": user.id_user, "name": user.name, "surname": user.surname})
            else:
                abort(405)
        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/organization/<organization_id>/user/<user_id>/', methods=['DELETE'])
def delUserOrg(organization_id, user_id):
    organization = Organization().get_organization(organization_id)
    if(organization):
        if(organization.exist_organization_user(user_id)):
            user = User().get_user(user_id)
            organization.delete_organization_user(user)

            return jsonify({"id_user": user.id_user, "name": user.name, "surname": user.surname})
        else:
            abort(404)
    else:
        abort(404)



#API Permiso-Usuario
@app.route('/api/v1.0/permission/<permission_id>/user/', methods=['GET'])
def getPermUsu(permission_id):

    permission = Permission().get_permission(permission_id)

    if(permission):
        users = User().get_permission_users(permission_id)
        jsonOut = []

        for user in users:
            jsonOut.append({
                "id_user": user.id_user,
                "name": user.name,
                "surname": user.surname
            })

        return json.dumps(jsonOut, indent=1, ensure_ascii=False).encode('utf8')

    else:
       abort(404)

