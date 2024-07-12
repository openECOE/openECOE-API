from . import socketio, chrono_app
from .classes import Manager
import json

from flask import render_template, request
from functools import wraps


def requires_tfc(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        tfc_header = request.headers.get('tfc')
        ecoe_id = ''
        if 'ecoe_id' in kwargs:
            ecoe_id = kwargs['ecoe_id']
        # # Only start if "tfc" is the same in the file and the param send
        if not check_tfc(tfc_header, ecoe_id):
            return 'Not authorized', 401
        else:
            return f(*args, **kwargs)

    return decorated


@chrono_app.route('/<int:station_id>/<int:round_id>')
def index(station_id, round_id):
    return render_template('index.html', station_id=station_id, round_id=round_id)


@chrono_app.route('/admin')
def admin():
    return render_template('admin.html', ecoes=chrono_app.ecoes)


@chrono_app.route('/abort/<int:ecoe_id>', methods=['POST'])
@requires_tfc
def abort_all(ecoe_id):
    ecoe = Manager.find_ecoe(ecoe_id)
    if ecoe is not None:
        for e_round in ecoe.rounds:
            e_round.abort()
            e_round.chrono.stop()
        return '', 200
    else:
        return 'ECOE %d not found'%ecoe_id, 404


def manage_chronos(active, ecoe_id, round_id):
    ecoe = Manager.find_ecoe(ecoe_id)

    if round_id is None:
        for e_round in ecoe.rounds:
            if active:
                e_round.chrono.activate()
            else:
                e_round.chrono.pause()
    else:
        e_rounds = [c for c in ecoe.rounds if c.id == round_id]

        if active:
            e_rounds[0].chrono.activate()
        else:
            e_rounds[0].chrono.pause()


@chrono_app.route('/pause/<int:ecoe_id>', methods=['POST'])
@chrono_app.route('/pause/<int:ecoe_id>/<int:round_id>', methods=['POST'])
@requires_tfc
def pause_chronos(ecoe_id, round_id=None):
    manage_chronos(active=False, ecoe_id=ecoe_id, round_id=round_id)
    return '', 200


@chrono_app.route('/play/<int:ecoe_id>', methods=['POST'])
@chrono_app.route('/play/<int:ecoe_id>/<int:round_id>', methods=['POST'])
@requires_tfc
def play_chronos(ecoe_id, round_id=None):
    manage_chronos(active=True, ecoe_id=ecoe_id, round_id=round_id)
    return '', 200


def has_threads_alive(ecoe_id):
    ecoe = Manager.find_ecoe(ecoe_id)
    if ecoe is None:
        return False
    else:
        return True in [t.is_alive() for t in ecoe.threads]


@chrono_app.route('/load', methods=['POST'])
def load_configuration():
    config = request.get_json()
    if 'ecoe' in config:
        ecoe_id = config['ecoe']['id']

        if not has_threads_alive(ecoe_id):

            Manager.create_config(config)

            return 'OK', 200
        else:
            return 'No cargado porque los cronos ya están iniciados', 409
    else:
        return 'Config error', 500


@chrono_app.route('/<int:ecoe_id>', methods=['DELETE'])
@requires_tfc
def delete_configuration(ecoe_id):
    if not has_threads_alive(ecoe_id):

        Manager.delete_config(ecoe_id)

        return 'OK', 200
    else:
        return 'No eliminado porque los cronos ya están iniciados', 409


@chrono_app.route('/start/<int:ecoe_id>', methods=['POST'])
@requires_tfc
def start_chronos(ecoe_id):
    if not has_threads_alive(ecoe_id):

        ecoe = Manager.find_ecoe(ecoe_id)

        if ecoe is not None:
            for e_round in ecoe.rounds:
                ecoe.threads.append(socketio.start_background_task(target=e_round.start))

            return 'OK', 200
        else:
            return 'ECOE %d not found' % ecoe_id, 404
    else:
        return 'Cronos ya iniciados', 409


def check_tfc(tfc, ecoe_id):
    ecoe = Manager.find_ecoe(ecoe_id)

    if ecoe is None:
        return False
    else:
        return tfc == ecoe.tfc


@chrono_app.route('/configurations')
@chrono_app.route('/configurations/<int:ecoe_id>')
def get_configurations(ecoe_id=None):
    configs = Manager.get_ecoe_config_files(ecoe_id)

    for conf in configs:
        # If tfc exists, remove from configurations info
        if 'tfc' in conf:
            del conf['tfc']

    return json.dumps(configs), 200

@chrono_app.route('/loop/<int:ecoe_id>', methods=['POST'])
@requires_tfc
def play_chrono_on_loop(ecoe_id=None):
    ecoe = Manager.find_ecoe(ecoe_id)
    if ecoe is None:
        return 'ECOE %d not found' % ecoe_id, 404
    
    body = request.get_json()
    if 'loop' not in body:
        return 'Request body error', 500
    
    loop = body['loop']

    for e_round in ecoe.rounds:
        e_round.chrono.loop = loop
    
    return 'OK', 200

@chrono_app.route('/rounds-status/<int:ecoe_id>')
def get_status(ecoe_id=None):
    ecoe = Manager.find_ecoe(ecoe_id)
    if ecoe is None:
        return 'ECOE %d not found' % ecoe_id, 404

    status = {}
    for e_round in ecoe.rounds:
        status[str(e_round.id)] = f"{e_round.chrono.state}"

    return json.dumps(status), 200

###############################

@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

################################
