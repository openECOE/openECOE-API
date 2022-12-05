import pandas as pd
from app.model import db
#This function gets all the data needed to generate the reports of each student
def get_students(id_ecoe):
    conexion = db.engine
    return pd.read_sql("""SELECT s.id, s.dni , s.surnames , s.name, s.planner_order , r.round_code,s2.shift_code 
    FROM student s 
    INNER JOIN planner p ON p.id = s.id_planner 
    INNER JOIN round r ON r.id = p.id_round 
    INNER JOIN shift s2  ON s2.id = p.id_shift 
    WHERE s.id_ecoe = """ + id_ecoe , conexion).rename(columns={'id':'id_student'})

