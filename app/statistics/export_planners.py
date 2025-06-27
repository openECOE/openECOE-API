import pandas as pd
from app.model import db

def get_students_planners(ecoe_id: int) -> pd.DataFrame: 
    connection=db.engine
    query = f""" SELECT sh.shift_code, sh.time_start , r.round_code, 
            e.name, e.surnames, e.dni, e.planner_order 
      FROM student e, planner p, round r, shift sh, ecoe
      WHERE e.id_planner = p.id 
        AND p.id_round = r.id 
        AND p.id_shift = sh.id 
        AND ecoe.id = {ecoe_id}
      ORDER BY e.planner_order;"""
    df = pd.read_sql(query, connection)
    return df