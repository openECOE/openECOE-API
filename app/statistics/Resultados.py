from collections import defaultdict
import pandas as pd
from app.model import db
from math import ceil



def preguntas(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q, station s WHERE q.id_station = s.id AND s.id_ecoe =" + id_ecoe, conexion)

def estudiantes(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT * FROM student WHERE id_ecoe = " + id_ecoe, conexion)

def resultados_evaluativo_ecoe(ecoe) -> dict:
    try:
        conexion = db.engine

        df_question = preguntas(ecoe) 
        df_student = estudiantes(ecoe).loc[:,['id','name','surnames','dni']]
        
        df_answer = pd.merge(
            left=df_student.rename(columns = {'id':'id_student'}),
            right=pd.read_sql("SELECT a.* FROM answer a, station s WHERE a.id_station = s.id AND s.id_ecoe =" + ecoe, conexion).loc[:,['id','id_student','id_question','points']].rename(
                columns = {'id':'id_answer'}), how='left',
            on=['id_student']).loc[:,['id_student','points']].fillna(0).groupby("id_student", as_index=False).sum()
        
        #NOTA ABSOLUTA, sumamos los puntos de las preguntas que hay en toda la ECOE
        total_points = df_question.loc[:,['max_points']].sum()['max_points']

        #NOTA RELATIVA, en función de la puntuación máxima sacada por un estudiante
        max_points =df_answer['points'].max()

        #Asignamos las notas relativas y absolutas usando de parámetro los calculado arriba
        df_answer = df_answer.assign(absolute_score = total_points).round(decimals=2).assign(
            relative_score = max_points).round(decimals=2).loc[:,['id_student','points','absolute_score','relative_score']]

        df_final = pd.merge(left=df_student.rename(columns = {'id':'id_student'}),
        right=df_answer,
        on=['id_student']).set_index('id_student', drop=False)
        dd = defaultdict(list)
        
        #order:: Orden segun las notas
        df_final['pos'] = df_final['points'].rank(method='min', ascending=False)
        #median:: Mediana de puntuación
        df_final = df_final.assign(median = df_final['points'].median())
        #perc:: Percentil de la columna punt
        df_final['perc'] = df_final['points'].rank(pct=True)
        df_final['perc'] = df_final['perc'].map(lambda x: ceil(x*10)*10)
        #Esto lo hemos usado para ver si rank funcionaba para generar el orden
        #TODO:: Pasar esto a ResultsForArea para que se genere de esta forma, y consultar con Alberto si asi es como lo queria mañana a primera hora
        #serie_cantidad = df_final.value_counts(subset=['pos'], sort=False)
        #numero_de_indexados = serie_cantidad.sum()
        cadena = df_final.to_dict('records',into=dd)
        
        return cadena
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error