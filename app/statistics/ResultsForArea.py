from collections import defaultdict
from math import ceil
import pandas as pd

from app.model import db


def get_students(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT s.id, s.name, s.surnames, s.dni  FROM student s WHERE s.id_ecoe = " + id_ecoe , conexion).rename(columns={'id':'id_student'})

def get_total_points(id_area):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q WHERE q.id_area = " + id_area, conexion).loc[:,['max_points']].sum()['max_points']

def get_answer(id_area, id_ecoe):
    conexion = db.engine
    df_all_students = get_students(id_ecoe)
    df_answering_students = pd.read_sql("SELECT a.* FROM answer a, question q WHERE a.id_question = q.id AND q.id_area  = " + id_area, conexion).loc[
        :,['id_student','points']].groupby("id_student", as_index=False).sum()
    df_alumnos = pd.merge(left=df_all_students, right=df_answering_students,how='left', on=['id_student']).fillna(0)
    return df_alumnos


def get_results_for_area(area,ecoe) -> pd.DataFrame:
    try:
        total_points = get_total_points(area)
        #if total_points = 0, there´s no questions asigned to this area, we return void to indicate this area isn´t being used and cant produce meaningfull info.
        if total_points == 0:
            return {}
        df_answer_area = get_answer(area,ecoe).assign(total_points = total_points)
        
        #max_points =df_answer_area['points'].max()
        #df_answer_area = df_answer_area.assign(max_points = max_points)

        #punt:: Porcentaje de acierto 
        df_answer_area = df_answer_area.assign(punt = df_answer_area['points']/total_points*100)
        #pos:: Posición en el orden por area de los alumnos
        df_answer_area['pos'] = df_answer_area['points'].rank(method='min', ascending=False)
        #med:: Mediana de puntuación
        df_answer_area = df_answer_area.assign(med = df_answer_area['punt'].median())
        #perc:: Percentil de la columna punt
        df_answer_area['perc'] = df_answer_area['points'].rank(pct=True).map(lambda x: ceil(x*10)*10)

        df_answer_area = df_answer_area.loc[:,['id_student','punt','pos','med','perc']]
        dd = defaultdict(list)
        cadena = df_answer_area.to_dict('records',into=dd)
        return cadena
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

   
#TODO:: Funciones para construir los resultados del informe internamente aqui en la API.
'''
def get_areas(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT a.id, a.name  FROM area a WHERE a.id_ecoe = " + id_ecoe , conexion)
    
def get_results_for_area_ecoe_areas(ecoe) -> list:
    try:
        df_areas = get_areas(ecoe)
        
       
        cadena = df_areas.values.tolist()
        
        return cadena          
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error 

def results_by_area(ecoe) -> list:
    try:
        areas = get_results_for_area_ecoe_areas(ecoe)
        
        lista_df =[]
        
        for id_area in areas:
            aux = get_results_for_area(area=str(id_area[0]))
            #Este if esta porque si una Area no tiene preguntas hace que crashee el proceso, por lo que si el area no tiene preguntas, lo ignoramos
            if( isinstance(aux, pd.DataFrame) ):
                lista_df.append( aux.rename(columns = {'punt':'punt_{}'.format(id_area[1]),'pos':'pos_{}'.format(id_area[1]),
                'med':'med_{}'.format(id_area[1]),'perc':'perc_{}'.format(id_area[1])}) ) 
        df_students = get_students(ecoe)
        for df_parcial in lista_df:
            df_students = pd.merge(left=df_students,
        right=df_parcial,
        on=['id_student'])
        
        #id_area = request.args.get('area')
        return df_students.to_html()  
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error
'''
