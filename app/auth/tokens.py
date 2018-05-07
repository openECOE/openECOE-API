from flask import jsonify, g
from flask_login import login_required, current_user
from app import db
from app.auth import bp


@bp.route('/tokens', methods=['POST'])
@login_required
def get_token():
    user_token = current_user.get_token()
    db.session.commit()
    return jsonify({'token': user_token.token, 'expiration': user_token.token_expiration})


@bp.route('/tokens', methods=['DELETE'])
@login_required
def revoke_token():
    current_user.revoke_token()
    db.session.commit()
    return '', 204
