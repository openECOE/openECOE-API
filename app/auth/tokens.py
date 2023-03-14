#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask import jsonify
from flask_login import current_user, login_required

from app.auth import bp
from app.model import db


@bp.route("/tokens", methods=["POST"])
@login_required
def get_token():
    user_token = current_user.get_token()
    db.session.commit()
    return jsonify(
        {"token": user_token.token, "expiration": user_token.token_expiration}
    )


@bp.route("/tokens", methods=["DELETE"])
@login_required
def revoke_token():
    current_user.revoke_token()
    db.session.commit()
    return "", 204
