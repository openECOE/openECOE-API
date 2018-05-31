from app import db


class ECOE(db.Model):
    __tablename__ = 'ecoe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    id_organization = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    areas = db.relationship('Area', backref='ecoe')
    stations = db.relationship('Station', backref='ecoe')
    schedules = db.relationship('Schedule', backref='ecoe')
    students = db.relationship('Student', backref='ecoe')
    rounds = db.relationship('Round', backref='ecoe')
    shifts = db.relationship('Shift', backref='ecoe')

    @property
    def configuration(self):

        stages = []
        stage_events = {}

        for sch in self.schedules:
            if sch.stage not in stages:
                stages.append(sch.stage)
                stage_events.update({sch.stage.id: []})

            for ev in sch.events:
                stage_events[sch.stage.id].append({
                    "t": ev.time,
                    "accion": ev.text,
                    "sound": ev.sound,
                    "estaciones": [0] + [station.id for station in self.stations] if sch.station is None else [sch.station.id],
                    "is_countdown": ev.is_countdown
                })

        stages.sort(key=lambda k: k.order)

        exists_dependant = False

        for station in self.stations:
            if station.parent_station is not None:
                exists_dependant = True
                break

        config = {
            "ruedas": [r.id for r in self.rounds],
            "vueltas": len(self.stations) + (1 if exists_dependant else 0),
            "planificaciones": [
                {'fase': st.name, 'duracion': st.duration, 'orden': st.order, 'eventos': stage_events[st.id]} for st in stages
            ]
        }

        return config



