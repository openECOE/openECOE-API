from app.model.Station import Station
from app.model.Area import Area

def get_variables(ecoe_id: int):
    variables =  {}
    descriptions = {}

    variables.update(get_variables_student(0))
    descriptions.update(get_variables_student(1))

    variables.update(get_variables_ecoe(0))
    descriptions.update(get_variables_ecoe(1))

    areas = Area.query.filter(Area.id_ecoe == ecoe_id)
    for area in areas:
        variables.update(get_variables_area(area.code, area.name, 0))
        descriptions.update(get_variables_area(area.code, area.name, 1))

    stations = Station.query.filter(Station.id_ecoe == ecoe_id)
    for station in stations:
        variables.update(get_variables_station(station.order, station.name, 0))
        descriptions.update(get_variables_station(station.order,station.name, 1))
    
    return variables, descriptions

def get_variables_area(code: str, name: str, option: int) -> dict:
    if option == 0:
        variables = {
            f"a{code}_mediana": f"a{code}_med",
            f"a{code}_percentile": f"a{code}_perc",
            f"a{code}_position": f"a{code}_pos",
            f"a{code}_punctuation": f"a{code}_punt"
        }
        return variables
    
    descriptions = {
            f"a{code}_mediana": f"{name} (Mediana)",
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
            f"e{order}_mediana": f"{name} (Mediana)",
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