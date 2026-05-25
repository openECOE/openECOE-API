import json

from chrono import chrono_app
from chrono.classes import Manager
from chrono.routes import reconcile_orphan_runtime


class DummyChrono:
    def __init__(self, status_filename):
        self.status_filename = status_filename
        self.stopped = False

    def stop(self):
        self.stopped = True


class DummyRound:
    def __init__(self, round_id, round_status_filename, chrono_status_filename):
        self.id = round_id
        self.status_filename = round_status_filename
        self.chrono = DummyChrono(chrono_status_filename)
        self.aborted = False

    def abort(self):
        self.aborted = True


class DummyEcoe:
    def __init__(self, ecoe_id, rounds):
        self.id = ecoe_id
        self.rounds = rounds
        self.threads = []


def test_reconcile_orphan_runtime_cleans_missing_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Manager, "path", f"{tmp_path}/")
    monkeypatch.setattr(Manager, "file_template", f"{tmp_path}/config_ecoe_%d.json")

    round_status_file = tmp_path / "round.1.status"
    chrono_status_file = tmp_path / "chrono.1.status"
    round_status_file.write_text(json.dumps({"state": "RUNNING"}), encoding="utf-8")
    chrono_status_file.write_text(json.dumps({"state": "RUNNING"}), encoding="utf-8")

    dummy_round = DummyRound(1, str(round_status_file), str(chrono_status_file))
    dummy_ecoe = DummyEcoe(10, [dummy_round])

    chrono_app.ecoes = [dummy_ecoe]

    reconcile_orphan_runtime(10)

    assert Manager.find_ecoe(10) is None
    assert dummy_round.aborted is True
    assert dummy_round.chrono.stopped is True
    assert not round_status_file.exists()
    assert not chrono_status_file.exists()


def test_reconcile_orphan_runtime_does_nothing_with_valid_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Manager, "path", f"{tmp_path}/")
    monkeypatch.setattr(Manager, "file_template", f"{tmp_path}/config_ecoe_%d.json")

    config_file = tmp_path / "config_ecoe_20.json"
    config_file.write_text(json.dumps({"ecoe": {"id": 20}}), encoding="utf-8")

    dummy_round = DummyRound(1, str(tmp_path / "round.20.status"), str(tmp_path / "chrono.20.status"))
    dummy_ecoe = DummyEcoe(20, [dummy_round])
    chrono_app.ecoes = [dummy_ecoe]

    reconcile_orphan_runtime(20)

    assert Manager.find_ecoe(20) is dummy_ecoe
