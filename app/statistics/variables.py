from app.model.Station import Station
from app.model.Area import Area

def get_variables(ecoe_id: int) -> dict:
    area_variables = {}
    area_descriptions = {}

    stations_variables = {}
    stations_descriptions = {}

    student_variables = get_variables_student(0)
    student_descriptions = get_variables_student(1)

    ecoe_variables = get_variables_ecoe(0)
    ecoe_descriptions = get_variables_ecoe(1)    

    global_results_variables = get_global_results_variables(0)
    global_results_descriptions = get_global_results_variables(1)

    areas = Area.query.filter(Area.id_ecoe == ecoe_id)
    for area in areas:
        area_variables.update(get_variables_area(area.code, area.name, 0))
        area_descriptions.update(get_variables_area(area.code, area.name, 1))

    stations = Station.query.filter(Station.id_ecoe == ecoe_id)
    for station in stations:
        stations_variables.update(get_variables_station(station.order, station.name, 0))
        stations_descriptions.update(get_variables_station(station.order,station.name, 1))
    
    variables = {
        'ecoe_variables': ecoe_variables, 
        'student_variables': student_variables,
        'area_variables': area_variables,
        'stations_variables': stations_variables,
        'global_results_variables': global_results_variables
    }

    descriptions = {
        'ecoe_descriptions': ecoe_descriptions, 
        'student_descriptions': student_descriptions,
        'area_descriptions': area_descriptions,
        'stations_descriptions': stations_descriptions,
        'global_results_descriptions': global_results_descriptions
    }

    d = {
        'variables': variables,
        'descriptions': descriptions
    }

    return d

def get_global_results_variables(option:str):
    if option == 0:
        variables = {
            "global_median": "glob_med",
            "global_percentile": "glob_perc",
            "global_position": "glob_pos",
            "global_punctuation": "glob_punt",
        }
        return variables

    descriptions = {
        "global_median": "Mediana global",
        "global_percentile": "Percentil global",
        "global_position": "Posición global",
        "global_punctuation": "Puntuación global",
    }
    return descriptions

def get_variables_area(code: str, name: str, option: int) -> dict:
    if option == 0:
        variables = {
            f"a{code}_median": f"a{code}_med",
            f"a{code}_percentile": f"a{code}_perc",
            f"a{code}_position": f"a{code}_pos",
            f"a{code}_punctuation": f"a{code}_punt"
        }
        return variables
    
    descriptions = {
            f"a{code}_median": f"{name} (Mediana)",
            f"a{code}_percentile": f"{name} (Percentil)",
            f"a{code}_position": f"{name} (Posición)",
            f"a{code}_punctuation": f"{name} (Puntuación)",
    }
    return descriptions


def get_variables_station(order: int, name: str, option: int) -> dict:
    if option == 0:
        variables = {
            f"e{order}_median": f"e{order}_med",
            f"e{order}_percentile": f"e{order}_perc",
            f"e{order}_position": f"e{order}_pos",
            f"e{order}_punctuation": f"e{order}_punt"
        }
        return variables

    descriptions = {
            f"e{order}_median": f"{name} (Mediana)",
            f"e{order}_percentile": f"{name} (Percentil)",
            f"e{order}_position": f"{name} (Posición)",
            f"e{order}_punctuation": f"{name} (Puntuación)",
    }
    return descriptions

def get_variables_student(option: int) -> dict:
    if option == 0:
        variables = {
            "student_name": "name",
            "student_surnames": "surnames",
            "student_full_name": "full_name",
            "student_dni": "dni",
        }
        return variables

    descriptions = {
        "student_name": "Nombre del estudiante",
        "student_surnames": "Apellidos del estudiante",
        "student_full_name": "Nombre completo del estudiante",
        "student_dni": "DNI del estudiante",
    }
    return descriptions

def get_variables_ecoe(option: int) -> dict:
    if option == 0:
        variables = {
            "ref_ecoe": "ref_ecoe",
            "date_ecoe": "date_ecoe"
        }
        return variables

    descriptions = {
        "ref_ecoe": "Referencia de la ECOE",
        "date_ecoe": "Fecha de la ECOE"
    }
    return descriptions