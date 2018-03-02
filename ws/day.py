from ws import *
from model import ECOE, Day

# RUTAS DE DIA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/', methods=['GET'])
def getDays(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        days = []

        for day in ecoe.days:
            days.append({
                "id_day" : day.id_day,
                "date" : day.date.strftime("%Y-%m-%d")
            })

        return json.dumps(days, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/<day_id>/', methods=['GET'])
def getDay(ecoe_id, day_id):
   day = Day().get_day(day_id)

   if(day==False):
       abort(404)

   if (ecoe_id==day.id_ecoe):
       return jsonify({"id_day": day.id_day, "date": day.date.strftime("%Y-%m-%d")})
   else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/', methods=['POST'])
def postDay(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        value = request.json

        # comprobar json
        if ((not request.json) or (not "date" in request.json)):
            abort(400)

        date = value["date"]

        dayIn = Day(date=date, id_ecoe=ecoe_id)
        dayIn.post_day()

        day = Day().get_last_day()

        return jsonify({"id_dia": day.id_day, "date": day.date.strftime("%Y-%m-%d")})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/<day_id>/', methods=['PUT'])
def putDay(ecoe_id, day_id):
    day = Day().get_day(day_id)

    if (day):
        if (ecoe_id != day.id_ecoe):
            abort(404)

        value = request.json

        if ((not request.json) or (not "date" in request.json) or (not "id_ecoe" in request.json)):
            abort(400)

        date = value["date"]
        id_ecoe = value["id_ecoe"]

        day.put_day(date, id_ecoe)

        return jsonify({"id_dia": day.id_day, "date": day.date.strftime("%Y-%m-%d")})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/day/<day_id>/', methods=['DELETE'])
def delDay(ecoe_id, day_id):
    day = Day().get_day(day_id)

    if (day):
        if (day.id_ecoe!=ecoe_id):
            abort(400)

        day.delete_day()
        return jsonify({"id_dia": day.id_day, "fecha": day.date.strftime("%Y-%m-%d")})
    else:
        abort(404)

