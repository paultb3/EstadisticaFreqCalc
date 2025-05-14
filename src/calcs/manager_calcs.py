import sys
import os
import pandas as pd
import numpy as np
# Agrega al path las rutas de los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importa tus módulos personalizados
import calcs.cuantitative_grouped_data as grouped
import calcs.cuantitative_no_grouped_data as no_grouped
from excception_handler import WarningException

import statistics

# =================== FUNCIONES DE GESTIÓN ===================
"""
Detecta si los datos son cuantitativos continuos o discretos.
"""
""" def detectar_tipo_dato(data):

    es_discreto = all(float(x).is_integer() for x in data)
    return "Discreto" if es_discreto else "Continuo"
"""
def Get_Results_For_Grouped_Data(data , precision):
    pass

def Get_Results_For_Not_Grouped_Data(data , precision):
    pass

def gestionar_datos(file_path, column_name , type_variable , precision):

    # Leer los datos desde Excel
    df = pd.read_excel(file_path)
    data = df[column_name].dropna().tolist()

    if not data:
        raise WarningException("No se encontraron datos para realizar los calculos.")

    """ tipo_dato = detectar_tipo_dato(data) """
    n = len(data)

    if type_variable == "Discreta":
        no_grouped.read_data_from_excel(file_path, column_name)
    elif type_variable == "Continua":
        m = 1 + (3.322*np.log10(n))
        if(m <= 5):
            grouped.read_data_from_excel(file_path, column_name)
        else:
            no_grouped.read_data_from_excel()
    else:
        raise WarningException("No se ha seleccionado el tipo de variable.")