from collections import defaultdict
import pandas as pd
from app.model import db




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
            right=pd.read_sql("SELECT a.* FROM answer a, station s WHERE a.id_station = s.id AND s.id_ecoe =" + ecoe, conexion).loc[:,['id','id_student','id_question','points']].rename(columns = {'id':'id_answer'}),
            on=['id_student']).loc[:,['id_student','points']].groupby("id_student", as_index=False).sum()
        
        #NOTA ABSOLUTA, sumamos los puntos de las preguntas que hay en toda la ECOE
        total_points = df_question.loc[:,['max_points']].sum()['max_points']

        #NOTA RELATIVA, en función de la puntuación máxima sacada por un estudiante
        max_points =df_answer['points'].max()

        #Asignamos las notas relativas y absolutas usando de parámetro los calculado arriba
        
        df_answer = df_answer.assign(absolute_score = total_points).assign(relative_score = max_points).loc[
                :,['id_student','points','absolute_score','relative_score']].round(
                {'absolute_score':2, 'relative_score':2})

        df_final = pd.merge(left=df_student.rename(columns = {'id':'id_student'}),
        right=df_answer,
        on=['id_student']).set_index('id_student', drop=False)
        dd = defaultdict(list)
        return  df_final.to_dict('records',into=dd)
        
        
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error