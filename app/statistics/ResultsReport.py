import pandas as pd
from app.statistics.ResultsForArea import results_by_area, get_areas_list
from app.statistics.Resultados import get_results_for_area_total
from app.model import db
from collections import defaultdict
import pdfkit
import jinja2
import os
from flask import current_app

def get_students(id_ecoe):
    conexion = db.engine
    return pd.read_sql("""SELECT s.id, s.dni , s.surnames , s.name, s.planner_order , r.round_code,s2.shift_code 
    FROM student s 
    INNER JOIN planner p ON p.id = s.id_planner 
    INNER JOIN round r ON r.id = p.id_round 
    INNER JOIN shift s2  ON s2.id = p.id_shift 
    WHERE s.id_ecoe = """ + id_ecoe , conexion).rename(columns={'id':'id_student'})

def generate_reports(id_ecoe, static_parameters):
    try:
        df_students = get_students(id_ecoe)
        df_results = results_by_area(id_ecoe)
        areas = get_areas_list(id_ecoe)
        df_results_total = get_results_for_area_total(id_ecoe)
        _med = df_results_total['med'][0]/df_results_total['absolute_score'][0]*100
        df_results_total['med'] = _med
        df_results_total = df_results_total.loc[:,['id_student','punt','pos','med','perc','absolute_score']]

        df_grades = pd.merge(left=df_results, right=df_results_total, on=['id_student'])
        df_final = pd.merge(left=df_students, right=df_grades, on=['id_student'])
        
        dd = defaultdict(list)
        raw_dict = df_final.to_dict('records',into=dd)
        listdict = []
        for dict in raw_dict:
            diccionario = {
                'dni':dict['dni'],
                'surnames':dict['surnames'],
                'name':dict['name'],
                'refECOE':str(dict['shift_code']) + str(dict['round_code']) + str(dict['planner_order']),
            }

            arealist = []

            for area in areas:
                diccionario_area={
                    "area":"{}".format(area[1]),
                    "punt":dict["punt_{}".format(area[1])],
                    "pos":dict["pos_{}".format(area[1])],
                    "med":dict["med_{}".format(area[1])],
                    "perc":dict["perc_{}".format(area[1])]
                }
                arealist.append(diccionario_area)

            #Total data
            diccionario_area={
                    "area":"Global de la prueba",
                    "punt":dict["punt"],
                    "pos":dict["pos"],
                    "med":dict["med"],
                    "perc":dict["perc"]
            }
            arealist.append(diccionario_area)

            diccionario["areas"] = arealist
            listdict.append(diccionario)

        templateLoader =jinja2.FileSystemLoader(searchpath=os.path.join(os.path.dirname(current_app.instance_path),  current_app.config.get("DEFAULT_TEMPLATE_ROUTE")))
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "results-report.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        
        #Static files that stay the same in every PDF
        img = os.path.join(os.path.dirname(current_app.instance_path),  current_app.config.get("DEFAULT_TEMPLATE_ROUTE")) + "/logo-umh.jpg"
        fondo = os.path.join(os.path.dirname(current_app.instance_path),  current_app.config.get("DEFAULT_TEMPLATE_ROUTE")) + "/fondo.jpg"
        css = os.path.join(os.path.dirname(current_app.instance_path),  current_app.config.get("DEFAULT_TEMPLATE_ROUTE")) + "/styles.css"
        options = {
            'page-size': 'Letter',
            'margin-top': '5px',
            'margin-right': '20px',
            'margin-bottom': '5px',
            'margin-left': '20px',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        urlarchive = os.path.join(os.path.dirname(current_app.instance_path),  current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))

        urlbase = urlarchive + "/ecoe-" + str(id_ecoe)
        import shutil
        if os.path.exists(urlbase):
            shutil.rmtree(urlbase)

        os.makedirs(urlbase)

        for informe in listdict:
            #Variables a sustituir
            outputText = template.render(**informe, **static_parameters, imagen=img, fondo=fondo)
            url = urlbase + "/grades-" + informe['refECOE'] + ".pdf"
            pdfkit.from_string(outputText, url, options=options, css=css)
        import shutil
        url_zip_absoluta = urlarchive + "/grades-ecoe" + str(id_ecoe)
        shutil.make_archive( url_zip_absoluta, 'zip', root_dir = urlbase, base_dir = "./")
        shutil.rmtree(urlbase)
        return True
        
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + str(arg)
        return "ko - Error: " + error

