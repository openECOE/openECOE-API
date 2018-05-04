from api import app

from flask import jsonify, request
import json
from werkzeug.exceptions import abort

from model import Permission, User

# TODO: chech this file (delete file?)

@app.route('/api/v1.0/permission/', methods=['GET'])
def getPermissions():
    permissions = []

    for permission in Permission.query.all():
        permissions.append({
            "id_permission": permission.id_permission,
            "id_typePermission": permission.id_typePermission,
            "id_organization": permission.id_organization,
            "id_ecoe": permission.id_ecoe,
            "id_station": permission.id_station
        })

    return json.dumps(permissions, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/permission/<permission_id>/', methods=['GET'])
def getPermission(permission_id):
    permission = Permission().get_permission(permission_id)

    if(permission):
        return jsonify({"id_permiso": permission.id_permission, "id_tipoPermiso": permission.id_typePermission, "id_organizacion": permission.id_organizacion, "id_ecoe": permission.id_ecoe, "id_estacion": permission.id_station})
    else:
        abort(404)

@app.route('/api/v1.0/permission/', methods=['POST'])
def postPermission():
    value = request.json

    if ((not request.json) or (not "id_typePermission" in request.json) or (not "id_organization" in request.json) or (not "id_ecoe" in request.json) or (not "id_station" in request.json)):
        abort(400)

    id_typePermission = value["id_tipoPermiso"]
    id_organization = value["id_organization"]
    id_ecoe = value["id_ecoe"]
    id_station = value["id_station"]

    permissionIn = Permission(id_typePermission, id_organization, id_ecoe, id_station)
    permissionIn.post_permission()

    permission = Permission().get_last_permission()
    return jsonify({"id_permiso": permission.id_permission, "id_tipoPermiso": permission.id_typePermission, "id_organization": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})


@app.route('/api/v1.0/permission/<permission_id>/', methods=['PUT'])
def actualizaPermiso(permission_id):
    permission = Permission().get_permission(permission_id)

    if(permission):
        value = request.json

        if ((not request.json) or (not "id_typePermission"  in request.json) or (not "id_organization" in request.json) or (not "id_ecoe" in request.json) or (not "id_station" in request.json)):
            abort(400)

        id_typePermission = value["id_typePermission"]
        id_organization = value["id_organization"]
        id_ecoe = value["id_ecoe"]
        id_station = value["id_station"]

        permission = Permission().get_permission(permission_id)
        permission.put_permission(id_typePermission, id_organization, id_ecoe, id_station)

        return jsonify({"id_permission": permission.id_permission, "id_typePermission": permission.id_typePermission, "id_organization": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})
    else:
        abort(404)


@app.route('/api/v1.0/permission/<permission_id>/', methods=['DELETE'])
def delPermission(permission_id):
    permission = Permission().get_permission(permission_id)

    if (permission):
        permission.delete_permission()
        return jsonify({"id_permission": permission.id_permission, "id_typePermission": permission.id_typePermission, "id_organization": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})
    else:
        abort(404)

#API Usuario-Permiso
@app.route('/api/v1.0/user/<user_id>/permission/', methods=['GET'])
def getPermUsers(user_id):
    user = User().get_user(user_id)

    if(user):
        permissions = []

        for permission in user.permissions:
            permissions.append({
                "id_permission": permission.id_permission,
                "id_typePermission": permission.id_typePermission,
                "id_organization": permission.id_organization,
                "id_ecoe": permission.id_ecoe,
                "id_station": permission.id_station
            })

        return json.dumps(permissions, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/user/<user_id>/permission/<permission_id>/', methods=['GET'])
def getPermUser(user_id, permission_id):
    user = User().get_user(user_id)

    if (user):
        if(user.exist_user_permission(permission_id)):
            permission = Permission().get_permission(permission_id)
            return jsonify(
                {"id_permission": permission.id_permission, "id_typePermission": permission.id_typePermission, "id_organization": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/user/<user_id>/permission/', methods=['POST'])
def postPermUser(user_id):
    user = User().get_user(user_id)

    if(user):
        value = request.json

        if ((not request.json) or (not "id_typePermission"  in request.json) or (not "id_organizacion" in request.json) or (not "id_ecoe" in request.json) or (not "id_station" in request.json)):
            abort(400)

        id_typePermission = value["id_typePermission"]
        id_organizacion = value["id_organizacion"]
        id_ecoe = value["id_ecoe"]
        id_station = value["id_station"]


        permissionIn = Permission(id_typePermission, id_organizacion, id_ecoe, id_station)
        permissionIn.post_permission()

        permission = Permission().get_last_permission()
        user.put_user_permission(permission)

        return jsonify({"id_permission": permission.id_permission, "id_typePermission": permission.id_typePermission, "id_organizacion": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})

    else:
        abort(404)


@app.route('/api/v1.0/user/<user_id>/permission/<permission_id>/', methods=['PUT'])
def putPermUser(user_id, permission_id):
    user = User().get_user(user_id)

    if(user):
        permission = Permission().get_permission(permission_id)
        if(permission):
            if(user.exist_user_permission(permission_id)==False):
                user.put_user_permission(permission)
                return jsonify({"id_permission": permission.id_permission , "id_typePermission": permission.id_typePermission, "id_organization": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_station": permission.id_station})
            else:
                abort(405)

        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/user/<user_id>/permission/<permission_id>/', methods=['DELETE'])
def eliminaUsuarioPerm(user_id, permission_id):
    user = User().get_user(user_id)
    if(user):
        if(user.exist_user_permission(permission_id)):
            permission = Permission().get_permission(permission_id)
            user.delete_user_permission(permission)

            return jsonify({"id_permission": permission.id_permission,"id_tipoPermiso": permission.id_typePermission, "id_organizacion": permission.id_organization, "id_ecoe": permission.id_ecoe, "id_estacion": permission.id_station})
        else:
            abort(404)
    else:
        abort(404)