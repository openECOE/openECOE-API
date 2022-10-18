from collections import defaultdict
from math import ceil
import pandas as pd
from app.api import area
from app.model import db


def get_students(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT s.id, s.name, s.surnames, s.dni  FROM student s WHERE s.id_ecoe = " + id_ecoe , conexion)

def get_areas(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT a.id  FROM area a WHERE a.id_ecoe = " + id_ecoe , conexion)

def preguntas(id_ecoe, id_area):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q, station s WHERE q.id_station = s.id AND s.id_ecoe =" + id_ecoe + " AND q.id_area = " + id_area, conexion)

def estudiantes(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT * FROM student WHERE id_ecoe = " + id_ecoe, conexion)

def get_total_points(id_area):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q WHERE q.id_area = " + id_area, conexion).loc[:,['max_points']].sum()['max_points']

def get_answer(id_area):
    conexion = db.engine
    return pd.read_sql("SELECT a.* FROM answer a, question q WHERE a.id_question = q.id AND q.id_area  = " + id_area, conexion).loc[:,['id_student','points']].groupby("id_student", as_index=False).sum()

def results_for_area(area) -> dict:
    try:
        total_points = get_total_points(area)
        df_answer_area = get_answer(area).assign(total_points = total_points)
        
        #max_points =df_answer_area['points'].max()
        #df_answer_area = df_answer_area.assign(max_points = max_points)

        #punt:: Porcentaje de acierto 
        df_answer_area = df_answer_area.assign(punt = df_answer_area['points']/total_points*100)
        #pos:: Posición en el orden por area de los alumnos
        df_answer_area = df_answer_area.sort_values(by=['points'], ascending=False).set_index(pd.Series(range(1, len(df_answer_area)+1) ) )
        df_answer_area.index.name = 'pos'
        df_answer_area = df_answer_area.sort_values(by=['id_student'], ascending=True).reset_index()
        #med:: Mediana de puntuación
        df_answer_area = df_answer_area.assign(med = df_answer_area['punt'].median())

        #perc:: Percentil de la columna punt
        df_answer_area['perc'] = df_answer_area['points'].rank(pct=True)
        df_answer_area['perc'] = df_answer_area['perc'].map(lambda x: ceil(x*10)*10)
        
        #return df_answer_area.to_html()

        df_answer_area = df_answer_area.loc[:,['id_student','punt','pos','med','perc']]
        
        dd = defaultdict(list)
        cadena = df_answer_area.to_dict('records',into=dd)
        
        return cadena
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

def results_for_area_ecoe_students(ecoe) -> dict:
    try:
        df_students = get_students(ecoe)
        
        dd = defaultdict(list)
        cadena = df_students.to_dict('records',into=dd)
        
        return cadena       
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

def results_for_area_ecoe_areas(ecoe) -> list:
    try:
        df_areas = get_areas(ecoe)
        
       
        cadena = df_areas.values.tolist()
        
        return cadena            

    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error