from collections import defaultdict
import pandas as pd

from app.model import db

def get_student_count(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT s.id  FROM student s WHERE s.id_ecoe = " + id_ecoe , conexion).count()['id']

def get_items_score(id_ecoe):
    conexion = db.engine
    pd_respuestas = pd.read_sql("SELECT q.id, q.id_station ,q.max_points , q.question_schema , a.points, s.name  FROM question q , answer a , station s WHERE a.id_question = q.id AND q.id_station = s.id AND a.id_station = s.id  AND s.id_ecoe = " + id_ecoe ,
     conexion).rename(columns={'id':'id_question', 'name':'station_name'})
    students = get_student_count(id_ecoe)

    pd_respuestas = pd_respuestas.groupby(['id_question','id_station','max_points','question_schema','station_name'])['points'].sum().reset_index()
    pd_respuestas['acierto'] = pd_respuestas['points']/(pd_respuestas['max_points'] * students)

    dd = defaultdict(list)
    
    return pd_respuestas.to_dict('records',into=dd)
    