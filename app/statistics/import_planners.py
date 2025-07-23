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
        """
        Crea nuevos estudiantes y los asocia a planificadores de forma masiva.
        Si un planificador (combinación de turno y ronda) no existe, lo crea.
        La operación es atómica: o todos se crean o no se crea ninguno.

        :param planners_to_import: Lista de diccionarios validados.
        """

        # print ("Has entrado en bulk_import_planners()")
        if not planners_to_import:
            return

        try:
            # 1. PRE-CARGA: Para evitar consultas en el bucle (muy eficiente).
            # Obtenemos todos los turnos y rondas necesarios en una sola consulta.
            planner_ids= {p['id_planner'] for p in planners_to_import}
            shift_codes = {p['shift_code'] for p in planners_to_import}
            round_codes = {p['round_code'] for p in planners_to_import}
            student_dnis = {p['dni'] for p in planners_to_import}
            
            planner_map = {p.id: p for p in db.session.query(Planner).filter(Planner.id.in_(planner_ids))}
            shifts_map = {s.shift_code: s for s in db.session.query(Shift).filter(Shift.shift_code.in_(shift_codes))}
            rounds_map = {r.round_code: r for r in db.session.query(Round).filter(Round.round_code.in_(round_codes))}
            students_map = {st.dni: st for st in db.session.query(Student).filter(Student.dni.in_(student_dnis))}

            # Obtenemos los planificadores que ya existen para este ECOE y los mapeamos.
            # La clave será una tupla (id_shift, id_round) para una búsqueda rápida.
            existing_planners = db.session.query(Planner).filter(Planner.id == self.id).all()
            planners_map = {(p.id_shift, p.id_round): p for p in existing_planners}

            # 2. CREACIÓN DE OBJETOS EN MEMORIA
            for data in planners_to_import:
                shift_obj = shifts_map.get(data['shift_code'])
                round_obj = rounds_map.get(data['round_code'])
                planner_obj = planners_map.get(data['id_planner'])

                # Si no encontramos el turno o la ronda, algo falló en la validación previa.
                if not shift_obj or not round_obj:
                    raise ValueError(f"No se encontró el turno '{data['shift_code']}' o la ronda '{data['round_code']}'")
                    return

                # Buscamos si el planificador ya existe.
                planner = planners_map.get((planner_obj, shift_obj, round_obj))

                # Si no existe, lo creamos en memoria y lo añadimos al mapa.
                if not planner:
                    planner = Planner(
                        id=planner_obj,
                        id_shift=shift_obj,
                        id_round=round_obj
                    )
                    db.session.add(planner) # El ORM lo añadirá a la transacción.
                    planners_map[(planner_obj, shift_obj, round_obj)] = planner

                student=db.session.query(Student).filter(
                    Student.dni == data['dni']
                ).first()
                student.id_planner=data['id_planner']
                student.planner_order=data['planner_order']

            # 3. COMMIT: Guardamos todos los cambios en la base de datos de una sola vez.
            db.session.commit()

        except Exception as e:
            # 4. ROLLBACK: Si algo falla, revertimos todos los cambios.
            db.session.rollback()
            # Propagamos la excepción para que la ruta la capture y devuelva un error 500.
            raise e