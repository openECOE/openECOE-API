from flask import jsonify, g
from flask_login import login_required, current_user
from app import db
from app.auth import bp
from app.auth.auth import token_auth


@bp.route('/tokens', methods=['POST'])
@login_required
def get_token():
    token = current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
