import pandas as pd
from math import ceil
from app.statistics.variables import get_global_results_variables, get_variables_area, get_variables_station

def get_report_data(ecoe_df: pd.DataFrame) -> pd.DataFrame:
    try:
        ecoe_df = ecoe_df[['student_id', 'dni', 'name', 'surnames', 
                       'station_order', 'area_code','question_id', 'question_max_points', 'answer_id', 'answer_points', 
                       'student_planner_order', 'round_code', 'shift_code' ]]
    except KeyError:
        print('All required columns are not present')
        return

    # Cuando un estudiante NO haya respondido una pregunta el valor de
    # los puntos de respuesta será 0 (antes NaN)
    ecoe_df['answer_points'].fillna(0)

    global_punctuation_df = get_global_punctuation(ecoe_df)
    
    global_statistics_df = calculate_global_statistics(global_punctuation_df)
    areas_statistics_df = calculate_statistics_by_area(ecoe_df)
    stations_statistics_df = calculate_statistics_by_station(ecoe_df)

    final_df = global_statistics_df.merge(areas_statistics_df, left_on='student_id', right_on='student_id')
    final_df = final_df.merge(stations_statistics_df, left_on='student_id', right_on='student_id')
    final_df['full_name'] = final_df['name'] + ' ' + final_df['surnames']
    final_df['ref_ecoe'] = final_df['shift_code'] + ' ' + final_df['round_code'] + ' ' + final_df['student_planner_order'].astype(str)
    final_df = final_df.round(2)
    return final_df

def get_question_statistics(ecoe_df: pd.DataFrame) -> pd.DataFrame:
    try:
        ecoe_df = ecoe_df[['student_id', 'station_id', 'station_order', 'station_name',
    'question_id', 'question_max_points', 'question_schema', 'answer_id', 'answer_points']]
    except KeyError:
        print('All required columns are not present')
        return

    n_students = ecoe_df['student_id'].nunique()
    results_df = ecoe_df.groupby(['question_id', 'station_id', 'station_name', 'question_schema']).apply(
        lambda gpd: pd.Series({
            'rate': (gpd['answer_points'].sum() / (gpd['question_max_points'].iloc[0] * n_students)) * 100 if gpd['question_max_points'].iloc[0] * n_students != 0 else 0
        })).reset_index()
    return results_df
    
def get_global_punctuation(ecoe_df: pd.DataFrame) -> pd.DataFrame:
    variables = get_global_results_variables(0)
    return ecoe_df.groupby(['student_id', 'dni', 'name', 'surnames', 'shift_code', 'round_code', 'student_planner_order']).apply(
        lambda gpd: pd.Series({
        variables['global_punctuation']: (gpd['answer_points'].sum() / gpd['question_max_points'].sum()) * 100 if gpd['question_max_points'].sum() != 0 else 0
        })).reset_index()

def calculate_global_statistics(global_punctuation_df: pd.DataFrame) -> pd.DataFrame:
    variables = get_global_results_variables(0)
    result_df = global_punctuation_df.copy()
    result_df[variables['global_median']] = result_df[variables['global_punctuation']].median()
    result_df[variables['global_percentile']] = result_df[variables['global_punctuation']].rank(pct=True).map(lambda x: ceil(x*10)*10)
    result_df[variables['global_position']] = result_df[variables['global_punctuation']].rank(method='min', ascending=False)
    
    # TODO: add the relative grades to the variables description
    max_points = result_df[variables['global_punctuation']].max() \
        if result_df[variables['global_punctuation']].max() != 0 else 0
    
    result_df[variables['relative_grade']] = result_df[variables['global_punctuation']] / max_points \
        if max_points != 0 else 0
    return result_df

def calculate_statistics_by_area(ecoe_df: pd.DataFrame) -> pd.DataFrame:
    grouped_df = ecoe_df.groupby(['student_id', 'area_code']).apply(
        lambda x: pd.Series({
            'punctuation': (x['answer_points'].sum() / x['question_max_points'].sum()) * 100 if x['question_max_points'].sum() != 0 else 0}))

    # Get areas
    areas = ecoe_df['area_code'].unique()

    # Each area will be a new column
    results_df = grouped_df.groupby(['student_id', 'area_code'])['punctuation'].first().unstack()
    results_df.reset_index(inplace=True)
    results_df.rename_axis(None, axis=1, inplace=True)
    
    for area_code in areas:
        variables = get_variables_area(area_code, None, 0)
        results_df[variables[f"a{area_code}_median"]] = results_df[area_code].median()
        results_df[variables[f"a{area_code}_percentile"]] = results_df[area_code].rank(pct=True).map(lambda x: ceil(x*10)*10)
        results_df[variables[f"a{area_code}_position"]] = results_df[area_code].rank(method='min', ascending=False)
        results_df.rename(columns={area_code: variables[f"a{area_code}_punctuation"]}, inplace=True)
    return results_df

def calculate_statistics_by_station(ecoe_df: pd.DataFrame) -> pd.DataFrame:
    grouped_df = ecoe_df.groupby(['student_id', 'station_order']).apply(
        lambda x: pd.Series({'punctuation': (x['answer_points'].sum() / x['question_max_points'].sum()) * 100 if x['question_max_points'].sum() != 0 else 0}))

    # Get stations
    stations = ecoe_df['station_order'].unique()

    # Each stations will be a new column
    results_df = grouped_df.groupby(['student_id', 'station_order'])['punctuation'].first().unstack()
    results_df.reset_index(inplace=True)
    results_df.rename_axis(None, axis=1, inplace=True)
    
    for station_order in stations:
        variables = get_variables_station(station_order, None, 0)
        results_df[variables[f"e{station_order}_median"]] = results_df[station_order].median()
        results_df[variables[f"e{station_order}_percentile"]] = results_df[station_order].rank(pct=True).map(lambda x: ceil(x*10)*10)
        results_df[variables[f"e{station_order}_position"]] = results_df[station_order].rank(method='min', ascending=False)
        results_df.rename(columns={station_order: variables[f"e{station_order}_punctuation"]}, inplace=True)
    
    return results_df

def get_items_score(questions_df: pd.DataFrame) -> pd.DataFrame:
    questions_df['answer_points'].fillna(0)
    item_score_df = get_question_statistics(questions_df)
    item_score_df = item_score_df.round(2)
    return item_score_df