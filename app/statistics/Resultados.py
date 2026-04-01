from collections import defaultdict
import pandas as pd
from app.model import db
from math import ceil
from app.statistics.ResultsForArea import results_by_area

def preguntas(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT q.* FROM question q, station s WHERE q.id_station = s.id AND s.id_ecoe =" + id_ecoe, conexion)

def estudiantes(id_ecoe):
    conexion = db.engine
    return pd.read_sql("SELECT * FROM student WHERE id_ecoe = " + id_ecoe, conexion)

def get_results_for_area_total(ecoe):
    conexion = db.engine
    try:
        df_question = preguntas(ecoe) 
        df_student = estudiantes(ecoe).loc[:,['id']]
        # Read raw answers to compute total points and number of correct answers (aciertos)
        answers_raw = pd.read_sql("SELECT a.* FROM answer a, station s WHERE a.id_station = s.id AND s.id_ecoe =" + ecoe, conexion).loc[:,['id','id_student','id_question','points']].rename(columns = {'id':'id_answer'})

        # Sum points per student
        df_points = answers_raw.groupby('id_student', as_index=False).agg(points=('points','sum'))
        # Count non-zero answers as 'aciertos'
        df_aciertos = answers_raw.groupby('id_student', as_index=False).agg(aciertos=('points', lambda x: (x > 0).sum()))

        # Merge with student list to include students with no answers
        df_answer = pd.merge(
            left=df_student.rename(columns = {'id':'id_student'}),
            right=df_points,
            how='left',
            on=['id_student']
        ).fillna(0)

        df_answer = pd.merge(df_answer, df_aciertos, how='left', on='id_student').fillna(0)
        
        #NOTA ABSOLUTA, sumamos los puntos de las preguntas que hay en toda la ECOE
        total_points = df_question.loc[:,['max_points']].sum()['max_points']        
        df_answer = df_answer.assign(absolute_score = total_points)
        #NOTA RELATIVA, en función de la puntuación máxima sacada por un estudiante
        max_points =df_answer['points'].max()
        df_answer = df_answer.assign(relative_score = max_points)

        #punt:: Puntuación del estudiante
        df_answer['punt'] = df_answer['points']/total_points*100
        #order:: Orden segun las notas
        df_answer['pos'] = df_answer['points'].rank(method='min', ascending=False)
        #median:: Mediana de puntuación
        _median = df_answer['points'].median()
        df_answer = df_answer.assign(med = _median)
        #perc:: Percentil de la columna punt
        df_answer['perc'] = df_answer['points'].rank(pct=True).map(lambda x: ceil(x*10)*10)

        df_answer['max_points'] = total_points
        # ensure integer counts
        df_answer['aciertos'] = df_answer['aciertos'].astype(int)
        return df_answer
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error

def resultados_evaluativo_ecoe(ecoe, datatype="dict") -> dict:
    try:
        df_answer = get_results_for_area_total(ecoe)
        df_student = estudiantes(ecoe).loc[:,['id','name','surnames','dni']]
        
        values_to_round = {'absolute_score':3, 'relative_score':3, 'nota_final':2}

        df_final = pd.merge(left=df_student.rename(columns = {'id':'id_student'}),
            right=df_answer,
            on=['id_student']).set_index('id_student', drop=False)
        
        # Obtener la nota global ponderada de results_by_area
        df_areas = results_by_area(ecoe)
        if isinstance(df_areas, pd.DataFrame) and 'nota_global' in df_areas.columns:
            df_final = pd.merge(
                left=df_final.reset_index(drop=True),
                right=df_areas[['id_student', 'nota_global']].rename(columns={'nota_global': 'nota_final'}),
                on='id_student',
                how='left'
            ).set_index('id_student', drop=False)
            df_final['nota_final'] = df_final['nota_final'].fillna(0)
        else:
            # Fallback: usar nota absoluta si no hay áreas con pesos
            df_final['nota_final'] = df_final['points'] / df_final['absolute_score'] * 100
        
        if datatype == "dict":  
            df_final = df_final.loc[
                :,['id_student','dni','name','surnames','points','absolute_score','relative_score','pos','med','perc', 'max_points', 'nota_final']].rename(columns={'med':'median'}).round(values_to_round)

            dd = defaultdict(list)
            return  df_final.to_dict('records',into=dd)

        
        

        df_final = df_final.rename(columns={'punt':'punt_total','pos':'pos_total','med':'med_total','perc':'perc_total'
        })
        #Hace falta acabar los cálculos que no va a realizar el frot si exportamos a fichero
        _median = df_answer['med'].values[0]
        _median = _median/df_answer['absolute_score'].values[0]*100
        df_final['med_total'] = _median
        df_final['absolute_score'] = df_final['points']/df_final['absolute_score']*10        
        df_final['relative_score'] = df_final['points']/df_final['relative_score']*10
        
        
        df_final = df_final.reindex(columns=['id_student','name','surnames','dni','points','absolute_score','relative_score',
        'punt_total','pos_total','med_total','perc_total'])
        df_areas = results_by_area(ecoe)
        df_final = pd.merge(left=df_final.reset_index(drop=True), right=df_areas.reset_index(drop=True), on=['id_student'])

        listacolumnas = list(df_final.columns.values)
        del listacolumnas[0:7]
        
        for indice, cadena in enumerate(listacolumnas):
            if (indice % 2) == 0:
                values_to_round[cadena] = 2
            if (indice % 4) == 1:
                df_final[cadena] = df_final[cadena].astype(int) 
            
        df_final = df_final.round(values_to_round)

        if datatype == "csv":
            import os
            from flask import current_app

            filename = "resultados_ecoe_" + ecoe + "." + datatype
            _archiveroute = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
            absolutefilepath = os.path.join(_archiveroute, filename)

            # Build CSV explicitly from students, answers and per-area results to avoid column mixups
            df_students = df_student.rename(columns={'id': 'id_student'})
            df_answers = df_answer.copy()

            # Merge students with answers
            export_df = pd.merge(df_students, df_answers[['id_student', 'points', 'aciertos', 'absolute_score', 'relative_score']], on='id_student', how='left').fillna(0)

            # Merge per-area data if available
            df_areas = results_by_area(ecoe)
            area_cols = []
            if isinstance(df_areas, pd.DataFrame) and not df_areas.empty:
                # capture punt_ columns (percent 0-100) and merge
                area_cols = [c for c in df_areas.columns if c.startswith('punt_')]
                export_df = pd.merge(export_df, df_areas, on='id_student', how='left').fillna(0)

            # Compute Nota final on 0-10 scale: prefer nota_global from areas if present
            if 'nota_global' in export_df.columns and export_df['nota_global'].notna().any():
                export_df['NotaFinal_10'] = export_df['nota_global'] / 10.0
            else:
                export_df['NotaFinal_10'] = (export_df['points'] / export_df['absolute_score'] * 100) / 10.0

            # Per-area notes scaled 0-10 from punt_<area> (which are percentages 0-100)
            per_area_export_cols = []
            for c in area_cols:
                col_name = f'Nota_{c.replace("punt_","")}_10'
                export_df[col_name] = export_df[c] / 10.0
                per_area_export_cols.append(col_name)

            # Relative grade 0-10: compute using relative_score (max_points) if present
            if 'relative_score' in export_df.columns and export_df['relative_score'].max() > 0:
                export_df['Nota_relativa_10'] = export_df['points'] / export_df['relative_score'] * 10
            elif 'max_points' in export_df.columns and export_df['max_points'].max() > 0:
                export_df['Nota_relativa_10'] = export_df['points'] / export_df['max_points'] * 10
            else:
                export_df['Nota_relativa_10'] = 0

            # Build final ordered column list
            ordered_cols = ['id_student', 'surnames', 'name', 'dni', 'aciertos', 'points', 'NotaFinal_10'] + per_area_export_cols + ['Nota_relativa_10']
            # Keep only existing columns
            ordered_cols = [c for c in ordered_cols if c in export_df.columns]

            out_df = export_df.loc[:, ordered_cols].copy()

            # Compute Aciertos as percentage of points / absolute_score (0-100)
            try:
                # build mapping from df_answers (original per-student totals)
                pct_map = {}
                if 'id_student' in df_answers.columns and 'points' in df_answers.columns and 'absolute_score' in df_answers.columns:
                    df_map = df_answers.set_index('id_student')
                    # avoid division by zero
                    for sid, row in df_map[['points', 'absolute_score']].iterrows():
                        try:
                            val = float(row['points']) / float(row['absolute_score']) * 100 if float(row['absolute_score']) > 0 else 0.0
                        except Exception:
                            val = 0.0
                        pct_map[sid] = "{:.2f}".format(round(val, 2)).replace('.', ',') + '%'
                # assign formatted percent to out_df based on id_student
                out_df['Aciertos'] = out_df['id_student'].map(lambda x: pct_map.get(x, '0,00%'))
            except Exception:
                out_df['Aciertos'] = '0,00%'

            # Remove raw 'aciertos' if present
            if 'aciertos' in out_df.columns:
                out_df = out_df.drop(columns=['aciertos'])

            # Ensure Aciertos column is positioned after 'dni'
            cols = out_df.columns.tolist()
            if 'Aciertos' in cols:
                cols.remove('Aciertos')
                if 'dni' in cols:
                    insert_at = cols.index('dni') + 1
                else:
                    insert_at = 4
                cols.insert(insert_at, 'Aciertos')
                out_df = out_df[cols]

            # Round all Nota* columns to 2 decimals
            nota_cols = [c for c in out_df.columns if c.startswith('Nota')]
            for c in nota_cols:
                try:
                    out_df[c] = out_df[c].astype(float).round(2)
                except Exception:
                    pass

            # Rename to Spanish headers
            rename_map = {
                'id_student': 'ID',
                'surnames': 'Apellidos',
                'name': 'Nombre',
                'dni': 'DNI',
                'points': 'Puntos',
                'NotaFinal_10': 'Nota final',
                'Nota_relativa_10': 'Nota relativa'
            }
            # area rename
            for c in per_area_export_cols:
                area_label = c.replace('Nota_', '').replace('_10', '').replace('_', ' ')
                rename_map[c] = f'Nota {area_label}'

            out_df = out_df.rename(columns=rename_map)
            out_df.to_csv(absolutefilepath, index=False, encoding='utf_8_sig', sep=';', quoting=1, decimal=',')

            return filename
    except Exception as err:
        for arg in err.args:
            error = ""
            error = error + arg
        return "ko - Error: " + error