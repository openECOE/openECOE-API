from collections import defaultdict
import pandas as pd
from app.model import db
from math import ceil
from app.statistics.ResultsForArea import results_by_area

def preguntas(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q, station s WHERE q.id_station = s.id AND s.id_ecoe =" + id_ecoe, conexion)

def estudiantes(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT * FROM student WHERE id_ecoe = " + id_ecoe, conexion)

def get_results_for_area_total(ecoe):
    conexion = db.engine
    try:
        df_question = preguntas(ecoe) 
        df_student = estudiantes(ecoe).loc[:,['id']]
        
        df_answer = pd.merge(
            left=df_student.rename(columns = {'id':'id_student'}),
            right=pd.read_sql("SELECT a.* FROM answer a, station s WHERE a.id_station = s.id AND s.id_ecoe =" + ecoe, conexion).loc[:,['id','id_student','id_question','points']].rename(
                columns = {'id':'id_answer'}), how='left',
            on=['id_student']).loc[:,['id_student','points']].fillna(0).groupby("id_student", as_index=False).sum()
        
        #NOTA ABSOLUTA, sumamos los puntos de las preguntas que hay en toda la ECOE
        total_points = df_question.loc[:,['max_points']].sum()['max_points']
        df_answer = df_answer.assign(absolute_score = total_points)
        #NOTA RELATIVA, en función de la puntuación máxima sacada por un estudiante
        max_points =df_answer['points'].max()
        df_answer = df_answer.assign(relative_score = max_points)

        #punt:: Puntuación del estudiante
        df_answer['punt'] = df_answer['points']/total_points*100
        #order:: Orden segun las notas
        df_answer['pos'] = df_answer['points'].rank(method='min', ascending=False)
        #median:: Mediana de puntuación
        _median = df_answer['points'].median()
        df_answer = df_answer.assign(med = _median)
        #perc:: Percentil de la columna punt
        df_answer['perc'] = df_answer['points'].rank(pct=True).map(lambda x: ceil(x*10)*10)

        return df_answer
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

def resultados_evaluativo_ecoe(ecoe, datatype="dict") -> dict:
    try:
        df_answer = get_results_for_area_total(ecoe)
        df_student = estudiantes(ecoe).loc[:,['id','name','surnames','dni']]
        
        values_to_round = {'absolute_score':3, 'relative_score':3}

        df_final = pd.merge(left=df_student.rename(columns = {'id':'id_student'}),
            right=df_answer,
            on=['id_student']).set_index('id_student', drop=False)
        
        if datatype == "dict":  
            df_final = df_final.loc[
                :,['id_student','dni','name','surnames','points','absolute_score','relative_score','pos','med','perc']].rename(columns={'med':'median'}).round(values_to_round)

            dd = defaultdict(list)
            return  df_final.to_dict('records',into=dd)

        
        

        df_final = df_final.rename(columns={'punt':'punt_total','pos':'pos_total','med':'med_total','perc':'perc_total'
        })
        #Hace falta acabar los cálculos que no va a realizar el frot si exportamos a fichero
        _median = df_answer['med'].values[0]
        _median = _median/df_answer['absolute_score'].values[0]*100
        df_final['med_total'] = _median
        df_final['absolute_score'] = df_final['points']/df_final['absolute_score']*10
        df_final['relative_score'] = df_final['points']/df_final['relative_score']*10
        
        
        df_final = df_final.reindex(columns=['id_student','name','surnames','dni','points','absolute_score','relative_score',
        'punt_total','pos_total','med_total','perc_total'])
        df_areas = results_by_area(ecoe)
        df_final = pd.merge(left=df_final.reset_index(drop=True), right=df_areas.reset_index(drop=True), on=['id_student'])

        listacolumnas = list(df_final.columns.values)
        del listacolumnas[0:7]
        
        for indice, cadena in enumerate(listacolumnas):
            if (indice % 2) == 0:
                values_to_round[cadena] = 2
            if (indice % 4) == 1:
                df_final[cadena] = df_final[cadena].astype(int) 
            
        df_final = df_final.round(values_to_round)

        if datatype == "csv":
            import os
            from flask import current_app

            filename = "resultados_ecoe_" + ecoe + "." + datatype
            _archiveroute = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
            absolutefilepath = os.path.join(_archiveroute, filename)
            df_final.to_csv(absolutefilepath,index=False,encoding='utf_8_sig',sep=';',quoting=1)

            return filename
        #TODO:: Add more export methods by comparing datatype with other strings

    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error