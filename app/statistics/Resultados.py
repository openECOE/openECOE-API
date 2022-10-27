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

def resultados_evaluativo_ecoe(ecoe, datatype="dict") -> dict:
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
        
        df_answer = df_answer.assign(absolute_score = total_points).assign(relative_score = max_points).loc[
                :,['id_student','points','absolute_score','relative_score']].round(
                {'absolute_score':2, 'relative_score':2})

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
        #serie_cantidad = df_final.value_counts(subset=['pos'], sort=False)
        #numero_de_indexados = serie_cantidad.sum()
        

        if datatype == "dict":
            return  df_final.to_dict('records',into=dd)
        
        #Hace falta acabar los cálculos que no va a realizar el frot si exportamos a fichero
        df_final['hit_rate'] = df_final['points']/df_final['absolute_score']*100
        df_final['absolute_score'] = df_final['points']/df_final['absolute_score']*10
        df_final['relative_score'] = df_final['points']/df_final['relative_score']*10
        df_final = df_final.round({'hit_rate':2, 'absolute_score':2, 'relative_score':2})
        #Añadimos aqui el porcentaje porque si no no se puede redondear
        df_final['hit_rate'] = df_final['hit_rate'].astype(str) + '%'
        df_final = df_final.reindex(columns=['id_student', 'surnames', 'name', 'dni', 'hit_rate','points','absolute_score','relative_score']).sort_values('points',ascending=False)
        
        import os
        from flask import current_app
        filename = "resultados_ecoe_" + ecoe + "." + datatype
        _archiveroute = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        absolutefilepath = os.path.join(_archiveroute, filename)
        
        if datatype == "csv":
            df_final.to_csv(absolutefilepath,index=False,encoding='utf-8')
            return filename
        #TODO:: Add more export methods by comparing datatype with other strings

    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error