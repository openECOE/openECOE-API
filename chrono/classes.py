from . import socketio, chrono_app
import json
import os



class Manager:
    path = '/tmp/'
    file_template = path + 'config_ecoe_%d.json'

    @staticmethod
    def create_config(config):
        ecoe = ECOE(config)

        chrono_app.ecoes.append(ecoe)
        filename = Manager.file_template % ecoe.id

        with open(filename, 'w') as f:
            json.dump(config, f)

        return ecoe

    @staticmethod
    def delete_config(ecoe_id):
        try:
            chrono_app.ecoes.remove(Manager.find_ecoe(ecoe_id))
        except ValueError:
            pass
        filename = Manager.file_template % ecoe_id
        Manager.delete_file(filename)

    @staticmethod
    def load_status_from_file(filename):
        status = {}

        try:
            with open(filename, 'r') as json_file:
                status = json.load(json_file)
        except FileNotFoundError:
            pass

        return status

    @staticmethod
    def delete_file(filename):

        try:
            os.remove(filename)
        except:
            pass

    @staticmethod
    def reload_status():

        ecoe_configs = Manager.get_ecoe_config_files()

        for ecoe_config in ecoe_configs:
            # 1. Create configuration in app memory
            ecoe = Manager.create_config(ecoe_config)

            # 2. Load objects
            for e_round in ecoe.rounds:
                try:
                    round_status = Manager.load_status_from_file(e_round.status_filename)

                    if len(round_status) > 0:

                        chrono_status = Manager.load_status_from_file(e_round.chrono.status_filename)

                        if len(chrono_status) > 0:
                            e_round.chrono.minutes = chrono_status['minutes']
                            e_round.chrono.seconds = chrono_status['seconds']
                            e_round.chrono.state = chrono_status['state']

                        ecoe.threads.append(socketio.start_background_task(target=e_round.start,
                                                                               state=round_status['state'],
                                                                               current_rerun=round_status['current_rerun'],
                                                                               idx_schedule=round_status['current_idx_schedule']))
                except:
                    pass

    @staticmethod
    def get_list_files(path):
        return os.listdir(path)

    @staticmethod
    def get_ecoe_config_files(ecoe_id=None):
        path = Manager.path
        files = Manager.get_list_files(path)
        configs = []
        if ecoe_id is not None:
            configs.append(Manager.load_status_from_file(path + Manager.file_template%ecoe_id))
        else:
            for file in files:
                if file.endswith('.json'):
                    conf = Manager.load_status_from_file(path + file)
                    configs.append(conf)

        return configs


    @staticmethod
    def find_ecoe(ecoe_id):
        return next((x for x in chrono_app.ecoes if x.id == ecoe_id), None)

class ECOE:
    def __init__(self, config):
        ecoe_config = config['ecoe']

        # Try to delete previous config
        Manager.delete_config(ecoe_config['id'])

        self.id = ecoe_config['id']
        self.name = ecoe_config['name']
        self.time_start = ecoe_config['time_start']
        self.tfc = config['tfc']
        self.rounds = []
        self.threads = []
        for r in config['rounds']:
            self.rounds.append(Round(r['id'], config['schedules'], config['reruns']))

class Round:
    CREATED = 0
    RUNNING = 1
    ABORTED = 2

    def __init__(self, id, schedules, num_reruns):
        self.id = id
        self.namespace = '/round%d' % id
        self.chrono = Chrono(id, self.namespace)
        self.schedules = schedules
        self.num_reruns = num_reruns
        self.state = Round.CREATED

    def abort(self):
        self.state = Round.ABORTED

    def is_aborted(self):
        return self.state == Round.ABORTED

    def dump(self, current_rerun, current_idx_schedule):

        status = {
            'state': self.state,
            'current_rerun': current_rerun,
            'current_idx_schedule': current_idx_schedule
        }

        with open(self.status_filename, 'w') as f:
            json.dump(status, f)

    @property
    def status_filename(self):
        return '/tmp/round.%d.status' % self.id

    def start(self, state=RUNNING, current_rerun=1, idx_schedule=0):

        self.state = state

        for n_rerun in range(current_rerun, self.num_reruns + 1):

            for schedule in self.schedules[idx_schedule:]:

                if self.is_aborted():
                    break

                socketio.emit('init_stage', {'num_rerun': n_rerun, 'total_reruns': self.num_reruns}, namespace=self.namespace)
                self.dump(n_rerun, idx_schedule)

                self.chrono.play(schedule, current_rerun=n_rerun, total_reruns=self.num_reruns)

                socketio.sleep(1)
                self.chrono.reset()

                idx_schedule += 1

            # reset index for next iteration
            idx_schedule = 0

            if self.is_aborted():
                socketio.emit('aborted', {}, namespace=self.namespace)
                break

        if not self.is_aborted():
            socketio.emit('end_round', {'data': 'Fin rueda %s' % self.id}, namespace=self.namespace)

        Manager.delete_file(self.status_filename)


class Chrono:
    CREATED = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3

    def __init__(self, id, namespace, minutes=0, seconds=0):
        self.id = id
        self.namespace = namespace
        self.minutes = minutes
        self.seconds = seconds
        self.state = Chrono.CREATED

    def reset(self):

        self.state = Chrono.CREATED
        self.minutes = 0
        self.seconds = 0

    def dump(self):

        status = {
            'minutes': self.minutes,
            'seconds': self.seconds,
            'state': self.state
        }

        with open(self.status_filename, 'w') as f:
            json.dump(status, f)

    @property
    def status_filename(self):
        return '/tmp/chrono.%d.status' % self.id

    def _create_tic_tac_dict(self, t, current_rerun, total_reruns, schedule):

        return {
            't': t,
            'minutes': '{:02d}'.format(self.minutes),
            'seconds': '{:02d}'.format(self.seconds),
            'stopped': 'S' if self.is_paused() else 'N',
            'num_rerun': current_rerun,
            'total_reruns': total_reruns,
            'stage': schedule
        }

    def play(self, schedule, current_rerun, total_reruns):

        duration = schedule['duration']
        events = schedule['events']
        stage_name = schedule['name']

        if self.state == Chrono.CREATED:
            self.activate()

        start_second = self.minutes * 60 + self.seconds

        for t in range(start_second, duration + 1):

            if self.state == Chrono.FINISHED:
                break

            if t % 60 == 0 and self.seconds == 59:
                self.minutes += 1
                self.seconds = 0
            else:
                self.seconds = t % 60

            tic_tac = self._create_tic_tac_dict(t, current_rerun, total_reruns, schedule)

            socketio.emit('tic_tac', tic_tac, namespace=self.namespace)
            self.dump()

            while self.is_paused():
                socketio.emit('tic_tac', tic_tac, namespace=self.namespace)
                socketio.sleep(0.5)

            # send events
            for e in events:
                if e['t'] == t:
                    # TODO: Change print values to UTF8 or use logger library
                    #print (time.strftime("%H:%M:%S") + " [%s] Rueda %d enviando evento en t = %d para %s" % (stage_name, self.id, t, ','.join(map(str, e['stations']))))
                    socketio.emit('evento',
                                  {
                                      'data': e['message'],
                                      'sound': e['sound'],
                                      'stage': schedule,
                                      'target': ','.join(map(str, e['stations']))
                                  },
                                  namespace=self.namespace)

            if t == duration:
                self.stop()
                break

            socketio.sleep(1)

    def activate(self):
        self.state = Chrono.RUNNING

    def stop(self):
        self.state = Chrono.FINISHED
        Manager.delete_file(self.status_filename)

    def pause(self):
        self.state = Chrono.PAUSED

    def is_paused(self):
        return self.state == Chrono.PAUSED
