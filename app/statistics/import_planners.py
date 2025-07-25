import pandas as pd
from app.model import db
from app.model import Planner, Shift, Round, Student



def get_row_student(dni, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM student
        WHERE id_ecoe={ecoe_id}
        AND dni={dni};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_student_rows_number(dni, ecoe_id: int) -> int:

    count = db.session.query(Student).filter_by(
        id_ecoe=ecoe_id,
        dni=dni
    ).count()

    return count

def get_row_round(round_code: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM round
        WHERE id_ecoe={ecoe_id}
        AND round_code={round_code};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_round_rows_number(round_code: int, ecoe_id: int) -> int:
    
    count = db.session.query(Round).filter_by(
        id_ecoe=ecoe_id,
        round_code=round_code
    ).count()

    return count

def get_row_shift(shift_code: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine

    query=f'''SELECT id FROM shift
        WHERE id_ecoe={ecoe_id}
        AND shift_code={shift_code};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_shift_rows_number(shift_code: int, ecoe_id: int) -> int:
    count = db.session.query(Shift).filter_by(
        id_ecoe=ecoe_id,
        shift_code=shift_code
    ).count()

    return count

def get_assigned_planners(id_planner :int, planner_order :int, ecoe_id :int) -> pd.DataFrame:
    connection = db.engine
    query=f'''SELECT id FROM student
            WHERE id_ecoe={ecoe_id}
            AND id_planner={id_planner}
            AND planner_order={planner_order};
    '''
    df = pd.read_sql(query, connection)
    return df

def get_assigned_planners_rows_number(id_planner :int, planner_order :int, ecoe_id :int) -> int:
    count = db.session.query(Student).filter_by(
        id_ecoe=ecoe_id,
        id_planner=id_planner,
        planner_order=planner_order
    ).count()
    return count

def set_student_in_planner(dni: int, id_planner: int, planner_order: int, ecoe_id: int) -> pd.DataFrame:
    connection = db.engine
    query=f'''UPDATE student
        SET id_planner={id_planner}, planner_order={planner_order}
        WHERE ecoe_id={ecoe_id} AND dni={dni};
    '''
    df = pd.read_sql(query,connection)
    return df

def add_planner(ecoe_id: int,id_planner: int, id_shift: int, id_round: int) -> pd.DataFrame:
    connection=db.engine
    query=f'''INSERT INTO planner (id, id_shift, id_round)
        VALUES ({id_planner},{id_shift},{id_round});
    '''
    df=pd.read_sql(query, connection)
    return df

def bulk_import_planners(self, planners_to_import: list[dict]):
    if not planners_to_import:
        return

    try:
        # 1. PRE-CARGA de datos relevantes
        shift_codes = {p['shift_code'] for p in planners_to_import}
        round_codes = {p['round_code'] for p in planners_to_import}
        student_dnis = {p['dni'] for p in planners_to_import}

        # Mapeamos por shift_code y round_code
        shifts_map = {s.shift_code: s for s in db.session.query(Shift).filter(Shift.shift_code.in_(shift_codes))}
        rounds_map = {r.round_code: r for r in db.session.query(Round).filter(Round.round_code.in_(round_codes))}
        students_map = {st.dni: st for st in db.session.query(Student).filter(Student.dni.in_(student_dnis))}

        # Mapeo de planificadores existentes (clave: (id_shift, id_round))
        existing_planners = db.session.query(Planner).all()
        planners_map = {(p.id_shift, p.id_round): p for p in existing_planners}
        
        existing_ids = {
            planner.id for planner in db.session.query(Planner.id).filter(
                Planner.id.in_({p['id_planner'] for p in planners_to_import})
            )
        }

        # 2. CREACIÓN EN MEMORIA
        for data in planners_to_import:
            shift_obj = shifts_map.get(data['shift_code'])
            round_obj = rounds_map.get(data['round_code'])

            if not shift_obj or not round_obj:
                raise ValueError(f"No se encontró el turno '{data['shift_code']}' o la ronda '{data['round_code']}'")

            planner = planners_map.get((shift_obj.id, round_obj.id))


            if not planner:
                if data['id_planner'] not in existing_ids:
                    planner = Planner(
                        id=data['id_planner'],  # Intentamos usar el ID propuesto si no existe
                        id_shift=shift_obj.id,
                        id_round=round_obj.id
                    )
                else:
                    planner = Planner(
                        id_shift=shift_obj.id,
                        id_round=round_obj.id
                    )
                db.session.add(planner)
                planners_map[(shift_obj.id, round_obj.id)] = planner

            student = students_map.get(data['dni'])
            if not student:
                raise ValueError(f"No se encontró ningún estudiante con DNI '{data['dni']}'")

            student.id_planner = planner.id
            student.planner_order = data['planner_order']

        # 3. COMMIT
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e