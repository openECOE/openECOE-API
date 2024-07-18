import pandas as pd
from app.model import db

def get_ecoe_data(ecoe_id: int) -> pd.DataFrame:
    connection = db.engine
    query = f"""SELECT student.id AS student_id,
        student.dni AS dni,
	    student.name AS name, 
        student.surnames AS surnames,
        student.planner_order AS student_planner_order,
	    question.id AS question_id, 
	    question.question_schema, 
	    question.max_points AS question_max_points,
	    answer.id AS answer_id, 
	    answer.answer_schema, 
	    answer.points AS answer_points,
	    area.id AS area_id,
	    area.name AS area_name,
        area.code AS area_code,
        station.id AS station_id,
        station.order AS station_order,
        station.name AS station_name,
	    round.id AS round_id, 
	    round.round_code, 
	    shift.id AS shift_id, 
	    shift.shift_code AS shift_code
    FROM ecoe
	    INNER JOIN student ON student.id_ecoe = ecoe.id
	    INNER JOIN area ON area.id_ecoe = ecoe.id
	    INNER JOIN question ON question.id_area = area.id
	    LEFT JOIN answer ON answer.id_question = question.id AND answer.id_student = student.id
	    INNER JOIN station ON station.id = question.id_station
	    INNER JOIN planner ON planner.id = student.id_planner
	    INNER JOIN shift ON shift.id = planner.id_shift
	    INNER JOIN round ON round.id = planner.id_round
    WHERE ecoe.id = {ecoe_id};"""

    df = pd.read_sql(query, connection)
    return df

def get_questions_data(ecoe_id: int) -> pd.DataFrame:
    connection = db.engine
    query = f"""SELECT station.id AS station_id,
		station.order AS station_order,
		station.name AS station_name,
		question.id AS question_id,
		question.max_points AS question_max_points,
		question.question_schema AS question_schema,
		answer.id AS answer_id,
		answer.points AS answer_points,
		student.id AS student_id
	FROM ecoe
		INNER JOIN student ON student.id_ecoe = ecoe.id
		INNER JOIN station ON station.id_ecoe = ecoe.id
		INNER JOIN question ON question.id_station = station.id
		LEFT JOIN answer ON answer.id_question = question.id AND answer.id_student = student.id
	WHERE ecoe.id = {ecoe_id};"""

    df = pd.read_sql(query, connection)
    return df