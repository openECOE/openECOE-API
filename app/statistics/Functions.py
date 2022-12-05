import pandas as pd
from app.model import db

#Suplementary functions used by some jobs related to the statistics module.

#Used by the endpoint Csv
#This function inserts a key-value pair in each of the dicts inside a list.
#key is taken as a parameter
#The value inserted into each dict is taken from a Pandas serie
def introducir_key_id(list_of_dictionary,serie_id, key):
    i = 0
    for dictionary in list_of_dictionary:
        dictionary[key]=serie_id.values[i,0]
        i = i + 1
    return list_of_dictionary

#Used by the endpoint ResultsReport
#This function gets all the data needed to generate the reports of each student
def get_students(id_ecoe):
    conexion = db.engine
    return pd.read_sql("""SELECT s.id, s.dni , s.surnames , s.name, s.planner_order , r.round_code,s2.shift_code 
    FROM student s 
    INNER JOIN planner p ON p.id = s.id_planner 
    INNER JOIN round r ON r.id = p.id_round 
    INNER JOIN shift s2  ON s2.id = p.id_shift 
    WHERE s.id_ecoe = """ + id_ecoe , conexion).rename(columns={'id':'id_student'})
