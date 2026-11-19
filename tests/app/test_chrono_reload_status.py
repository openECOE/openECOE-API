import json

from chrono import chrono_app
from chrono import classes
from chrono.classes import Manager, Status


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_reload_status_restores_paused_chrono_from_chrono_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(Manager, "path", f"{tmp_path}/")
    monkeypatch.setattr(Manager, "file_template", f"{tmp_path}/config_ecoe_%d.json")
    chrono_app.ecoes = []

    started = []
    monkeypatch.setattr(classes.socketio, "start_background_task",
                        lambda target, **kwargs: started.append((target, kwargs)))

    _write(tmp_path / "config_ecoe_7.json", {
        "ecoe": {"id": 7, "name": "ECOE", "organization": 1, "time_start": None},
        "rounds": [{"id": 3}],
        "schedules": [],
        "reruns": 2,
        "tfc": None,
    })
    _write(tmp_path / "round.3.status", {"state": "RUNNING", "current_rerun": 2, "current_idx_schedule": 1})
    _write(tmp_path / "chrono.3.status", {"minutes": 4, "seconds": 30, "state": "PAUSED"})

    Manager.reload_status()

    ecoe = Manager.find_ecoe(7)
    e_round = ecoe.rounds[0]
    assert e_round.status_filename == f"{tmp_path}/round.3.status"
    assert e_round.chrono.status_filename == f"{tmp_path}/chrono.3.status"
    assert e_round.chrono.state is Status.PAUSED
    assert e_round.chrono.is_paused()
    assert (e_round.chrono.minutes, e_round.chrono.seconds) == (4, 30)

    assert len(started) == 1
    target, kwargs = started[0]
    assert target == e_round.start
    assert kwargs == {"state": Status.RUNNING, "current_rerun": 2, "idx_schedule": 1}

    chrono_app.ecoes = []
