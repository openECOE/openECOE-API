#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from app.model import Organization
from flask import Blueprint, send_file

bp = Blueprint('statistics', __name__)

#Esta función introduce en una lista de diccionarios un par clave(=atributo "key")-valorid(=serie_id) 
def introducir_key_id(list_of_dictionary,serie_id, key):
    i = 0
    for dictionary in list_of_dictionary:
        dictionary[key]=serie_id.values[i,0]
        i = i + 1
    return list_of_dictionary

#Esta función convierte diccionarios con clave "selected" en listas de diccionarios, haciendo que los datos queden juntos
def convert(dictionary):
    for key in dictionary:
        if key == "selected" and isinstance(dictionary[key], list)==False:
            dictionary[key] = [dictionary[key]]
    return dictionary

#http://127.0.0.1:5000/statistics para acceder a esta ruta
@bp.route("/", methods=['GET', 'POST'])
def statistics():
    try:
        import numpy as np
        import pandas as pd
        from app.model import db
        import json
        #conexion = db.engine.connect().connection
        conexion = db.engine
        #Medimos el tiempo de ejecucion
        import time
        inicio = time.time()

        #df_organization = pd.read_sql("SELECT * FROM shift", organization)
        #df_ecoe = pd.read_sql("SELECT * FROM shift", ecoe)
        df_ecoe_organization = pd.merge(left=pd.read_sql_table("ecoe", conexion).rename(columns = {'id':'id_ecoe','name':'ecoe_name',
        'status':'ecoe_status','chrono_token':'ecoe_chrono_token'}),
        right=pd.read_sql_table("organization", conexion).rename(columns = {'id':'id_organization',
        'name':'organization_name'}), on=['id_organization'])
        df_ecoe = pd.merge(left=df_ecoe_organization,
        right=pd.read_sql_table("user", conexion).loc[:,['id','name','surname','email']].rename(columns = {
        'id':'id_coordinator', 'name':'coordinator_name','surname':'coordinator_surname','email':'coordinator_email'}),
         on=['id_coordinator'])
        
        #df_planner = pd.read_sql("SELECT * FROM planner", conexion)
        df_planner_shift = pd.merge(left=pd.read_sql_table("planner", conexion).rename(columns = {'id':'id_planner'}), 
        right=pd.read_sql_table("shift", conexion).rename(columns = {'id':'id_shift','time_start':'shift_time_start'}),
         on='id_shift')
        df_planner = pd.merge(left=df_planner_shift, right=pd.read_sql_table("round", conexion)
        .rename(columns = {'id':'id_round','description':'round_description'}), on=['id_round','id_ecoe'])
        
        #df_student = pd.read_sql("SELECT * FROM student", conexion)
        df_student = pd.merge(left=df_planner, right=pd.read_sql_table("student", conexion).rename(
        columns = {'id':'id_student','name':'student_name','surnames':'student_surnames','dni':'student_dni','planner_order':'student_planner_order'}),
         on=['id_planner','id_ecoe'])
        
        
        #df_question = pd.read_sql("SELECT * FROM question", conexion)
        #Vamos a intentar normalizar por partes
        #df_question_original = pd.read_sql("SELECT * FROM question", conexion)   
        df_question_original = pd.read_sql_table("question", conexion)  
        #Quita las comillas excesivas que envolvian cada diccionario sin causar errores
        listadict = df_question_original.loc[:,"question_schema"].values.tolist()
        listadict = list(map(json.loads, listadict))
        serie_ids = df_question_original.loc[:,["id"]]
        listadict = introducir_key_id(listadict, serie_ids, "id_question")
        pddict = pd.json_normalize(listadict, errors='ignore').rename(columns = {'reference':'question_reference','description':'question_description'})

        df_question_normalizada = pd.merge(left=pd.read_sql("SELECT * FROM question", conexion).rename(columns = {'id':'id_question','order':'question_order',
        'max_points':'question_max_points'}), right=pddict, on='id_question')[['id_question','id_area','question_order','id_block','id_station','question_max_points',
        'question_reference','question_description']]

        #df_area = pd.read_sql("SELECT * FROM area", conexion)
        df_question_area = pd.merge(left=df_question_normalizada, right=pd.read_sql_table("area", conexion).rename(columns = {'id':'id_area','name':'area_name',
        'code':'area_code'}), on='id_area')

        #df_station = pd.read_sql("SELECT * FROM station", conexion)
        df_station_manager = pd.merge(
        left=pd.read_sql_table("station", conexion).rename(columns = {
        'id':'id_station','name':'station_name', 'code':'area_code', 'order':'station_order'}),
        right=pd.read_sql_table("user", conexion).loc[:,['id','name','surname','email']].rename(columns={
        'id':'id_manager','name':'manager_name','surname':'manager_surname','email':'manager_email'}), on='id_manager')
        
        df_station = pd.merge(
        left=df_station_manager,
        right=df_station_manager.loc[:,['id_station','station_name']].rename(columns={'id_station':'id_parent_station',
        'station_name':'station_parent_station_name'}), on='id_parent_station', 
        how="left")

        df_question_area_station = pd.merge(left=df_question_area, right=df_station, on=['id_station','id_ecoe'])
        
        df_question = pd.merge(left=df_question_area_station, right=pd.read_sql_table("block", conexion).loc[:,['id','name','order']].rename(
        columns={'id':'id_block','name':'block_name','order':'block_order'}), on=['id_block'])
        
        #df_answer = pd.read_sql("SELECT * FROM answer", conexion)
        #Esto lo podemos poner al final, mete el tipo de pregunta como una columna más a la tabla, pero hace que tarde mucho mas
        
        df_answer_original = pd.read_sql_table("answer", conexion)
        listadict2 = df_answer_original.loc[:,"answer_schema"].values.tolist()
        listadict2 = list(map(json.loads, listadict2))
        serie_ids2 = df_answer_original.loc[:,["id"]]
        listadict2 = introducir_key_id(listadict2, serie_ids2, "id_answer")
        pddict2 = pd.json_normalize(listadict2, errors='ignore')
        df_answer_normalizada = pd.merge(left=pd.read_sql_table("answer", conexion).rename(columns = {'id':'id_answer'}),
        right=pddict2, on='id_answer')[['id_answer','id_student','id_question','answer_schema','points','id_station',
        'type']].rename(columns = {'type':'answer_type'})
        df_answer_student = pd.merge(left=df_answer_normalizada.rename(columns = {'points':'answer_points'}),
        right=df_student, on='id_student')
        """
        df_answer_student = pd.merge(left=pd.read_sql_table("answer", conexion).rename(columns = {'points':'answer_points'}),
        right=df_student, on='id_student')
        """
        df_answer_student_question = pd.merge(left=df_answer_student,
        right=df_question, on=['id_question','id_station','id_ecoe']).rename(columns = {'id':'id_answer'})
        
        
        df_answer = pd.merge(left=df_answer_student_question,
        right=df_ecoe, on=['id_ecoe']).rename(columns = {'id':'id_answer'})
        
        #Formateo para que los datos sean mas legibles
        #TODO Seguir cambiando estos indices para dejarlos de la forma mas legible y luego pasar a CSV
        df_answer = df_answer.reindex(columns=['organization_name',
        'ecoe_name', 'ecoe_status', 'ecoe_chrono_token',
        'round_code', 'round_description',
        'shift_code', 'shift_time_start',

        'block_name', 'block_order',
        'question_order', 'question_reference', 'question_description',
        'area_name', 'area_code',
        'answer_schema','answer_type',
        'answer_points','question_max_points',
        
        'student_name','student_surnames', 'student_dni', 'student_planner_order',
        
        'station_name', 'station_order','station_parent_station_name',
        'manager_name', 'manager_surname','manager_email',
        'coordinator_name', 'coordinator_surname', 'coordinator_email',
        'id_answer', 'id_student','id_question', 'id_station', 'id_planner', 'id_shift', 'id_round',
        'id_ecoe', 'id_area', 'id_block', 'id_parent_station', 'id_manager','id_organization','id_coordinator'])

        #listadict = pddict.loc[:,"selected"].values.tolist()
        #listadict = df_answer.loc[:,"answer_schema"].values.tolist()
        #pddict = pd.json_normalize(listadict,'selected',errors='ignore')
        #cadena = df.to_string(index=False)
        #cadena = df.to_html(index=False)
        
        cadena = "Dimensiones de df_answer (filas, columnas) = (" + str(df_answer.shape[0]) + "," + str(df_answer.shape[1]) +")\n"
        cadena = cadena + "<p>df_answer</p>" + df_answer.head().to_html(index=False)
        #cadena = cadena + "Datos cadena:   " + str(df_question["question_schema"].describe())
        #Mostrar lista de diccionarios con la que hemos acabado la ejecución
        #cadena = cadena + "<p>listadict</p>" + str(listadict)
        #cadena = cadena + "<p>serie_ids</p>" + serie_ids.head().to_html()
        #cadena = cadena + "<p>df_ecoe</p>" + df_ecoe.head().to_html(index=False)
        #cadena = cadena + "<p>pddict  _max_points</p>" + pddict.iloc[1812:,:].head().to_html(index=False)
        #cadena = cadena + "<p>pddict  range</p>" + pddict.iloc[155:160,:].head().to_html(index=False)
        
        #Mostramos el tiempo de ejecucion
        fin = time.time()
        tejecucion = fin-inicio
        cadena = cadena + "Tiempo de ejecución = " + str(tejecucion) + " segundos"

        import io
        buf = io.StringIO()
        df_answer.info(buf=buf)
        s = buf.getvalue()
        s = s.replace("\n","<br>")
        s = s.replace("         ","&emsp;")
        cadena = cadena + s
        df_answer.to_csv("app/ficheros/datos_estadistica.csv",index=False,encoding='utf-8')
        return send_file("ficheros/datos_estadistica.csv", as_attachment=True)
        #return cadena
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

@bp.route("/download", methods=['GET', 'POST'])
def download():
        
        return send_file("ficheros/datos_estadistica.csv", as_attachment=True)