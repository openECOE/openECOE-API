import pandas as pd
from app.model import db


def get_row_student(dni, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM student
        WHERE id_ecoe={ecoe_id}
        AND dni={dni};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_row_round(round_code: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM round
        WHERE id_ecoe={ecoe_id}
        AND round_code={round_code};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_row_shift(shift_code: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM shift
        WHERE id_ecoe={ecoe_id}
        AND shift_code={shift_code};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_assigned_planners(planner_id :int, planner_order :int, ecoe_id :int) -> pd.DataFrame:
    connection = db.engine
    query=f'''SELECT id FROM student
            WHERE id_ecoe={ecoe_id}
            AND planner_id={planner_id}
            AND planner_order= {planner_order};
    '''
    df = pd.read_sql(query, connection)
    return df

def set_student_in_planner(dni: int, planner_id: int, planner_order: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine
    query=f'''UPDATE student
        SET planner_id={planner_id}, planner_order={planner_order}
        WHERE ecoe_id={ecoe_id} AND dni={dni};
    '''
    df = pd.read_sql(query,connection)
    return df

def add_planner(ecoe_id: int) -> pd.DataFrame:
    df=pd.read_sql
    return df



def get_row_imports(dataframe) -> pd.DataFrame:
    dataframe
    
    return pd
    