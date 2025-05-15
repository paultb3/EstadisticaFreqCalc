import sys
import os
import pandas as pd
import numpy as np
# Agrega al path la raíz del proyecto para que los imports funcionen correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importa tus módulos personalizados
import cuantitative_grouped_data as grouped
import cuantitative_no_grouped_data as no_grouped
# =================== FUNCIONES DE GESTIÓN ===================
def Get_Results_For_Grouped_Data(data, precision):
    # Calcular valores básicos
    n = len(data)
    vmin = grouped.find_min(data)
    vmax = grouped.find_max(data)
    rango = grouped.find_range(data)
    m = grouped.calculate_m(n)
    m_redondeado = grouped.round_m(m)
    amplitud = grouped.calculate_amplitude(rango, precision)
    intervals = grouped.calc_intervals(vmin, amplitud, precision)
    fi = grouped.calc_fi(data, intervals)
    fi_cum = grouped.calc_fi_cumulative(fi)
    hi = grouped.calc_hi(fi, n)
    hi_cum = grouped.calc_hi_cumulative(hi)
    pi = grouped.calc_pi_percent(hi)
    pi_cum = grouped.calc_pi_cumulative(pi)
    midpoints = grouped.calc_midpoints(intervals)
    mean = grouped.calc_mean(midpoints, fi, n)
    median = grouped.calc_median(intervals, fi, n, amplitud)
    mode = grouped.calc_mode(intervals, fi, amplitud)

    # Retornar todos los resultados en un diccionario
    return {
        'vmin': vmin,
        'vmax': vmax,
        'rango': rango,
        'n': n,
        'm': m,
        'm_redondeado': m_redondeado,
        'amplitud': amplitud,
        'intervalos': intervals,
        'fi': fi,
        'fi_cum': fi_cum,
        'hi': hi,
        'hi_cum': hi,
        'pi': pi,
        'pi_cum': pi_cum,
        'midpoints': midpoints,
        'mean': mean,
        'median': median,
        'mode': mode
    }

def Get_Results_For_Not_Grouped_Data(data):
    # Calcular estadísticas básicas y tabla de frecuencias
    tabla_frecuencias = no_grouped.calcular_tabla_frecuencias(data)
    estadisticas = no_grouped.calcular_estadisticas(data)
    return {
        'tabla_frecuencias': tabla_frecuencias,
        'estadisticas': estadisticas
    }
def read_data_from_excel(file_path, column_name):
    df = pd.read_excel(file_path)
    return df[column_name].dropna().tolist()

def gestionar_datos(file_path, column_name , type_variable , precision):

    # Leer los datos desde Excel
    df = pd.read_excel(file_path)
    data = df[column_name].dropna().tolist()

    results = {}

    if not data:
        raise Exception("No se encontraron datos para realizar los calculos.")

    """ tipo_dato = detectar_tipo_dato(data) """
    n = len(data)

    if type_variable == "Discreta":
        data = read_data_from_excel(file_path, column_name)
        results = Get_Results_For_Not_Grouped_Data(data)
        return results
    elif type_variable == "Continua":
        m = 1 + (3.322*np.log10(n))
        if(m >= 5):
            data = read_data_from_excel(file_path, column_name)
            results = Get_Results_For_Grouped_Data(data, precision)
            return results
        else:
            results = Get_Results_For_Not_Grouped_Data(data)
            return results
    else:
        raise  Exception("No se ha seleccionado el tipo de variable.")