import sys
import os
# Agrega al path la raíz del proyecto para que los imports funcionen correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import numpy as np

# Importa tus módulos personalizados
import cuantitative_grouped_data as grouped
import cuantitative_no_grouped_data as no_grouped
from tkinter import filedialog

# =================== FUNCIONES DE GESTIÓN ===================
def Find_Max_Decimal_Number_In_Dataset(Data):
    N_Decimals = []
    for data in Data:
        if("." in str(data)):
            N_Decimals.append(len(str(data).split(".")[1]))
        else:
            N_Decimals.append(0)
    return np.max(N_Decimals)

def Get_Results_For_Grouped_Data(data):
    # Calcular valores básicos
    n = len(data)
    vmin = grouped.find_min(data)
    vmax = grouped.find_max(data)
    rango = grouped.find_range(data)
    m = grouped.calculate_m(n)
    m_redondeado = grouped.round_m(m)

    max_n_decimals_in_data = Find_Max_Decimal_Number_In_Dataset(data)

    amplitud , N_Decimals_C = grouped.calculate_amplitude(rango, m_redondeado , max_n_decimals_in_data)

    intervals = grouped.calc_intervals(vmin, amplitud, m_redondeado , N_Decimals_C)

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
            "Base_Results": {
                'vmin': vmin,
                'vmax': vmax,
                'rango': rango,
                'n': n,
                'm': m_redondeado,
                'amplitud': amplitud,
            },
            "Frecuences_Results":{
                'intervalos': intervals,
                'xi': midpoints,
                'fi': fi,
                'Fi': fi_cum,
                'hi': hi,
                'Hi': hi_cum,
                'pi': pi,
                'Pi': pi_cum,
            },
            "Centray_Tendency_Measures":{
                'X_': mean,
                'Me': median,
                'Mo': mode,
            }
        }

def Get_Results_For_Not_Grouped_Data(data):
    # Calcular estadísticas básicas y tabla de frecuencias
    n = len(data)

    Arr_xi , Arr_fi = no_grouped.Calc_fi_and_xi(data)
    Arr_Fi = no_grouped.Calc_Fi(Arr_fi)

    Arr_hi = no_grouped.Calc_hi(Arr_fi , n)
    Arr_Hi = no_grouped.Calc_Hi(Arr_hi)

    Arr_pi = no_grouped.Calc_pi_percent(Arr_hi)
    Arr_Pi = no_grouped.Calc_Pi_percent(Arr_pi)

    X_ = no_grouped.Calc_Atihmetic_Average(data)
    Me = no_grouped.Calc_Median(data)
    Mo = no_grouped.Calc_Mode_Mo(Arr_xi , Arr_fi)
    

    S_2 = no_grouped.Calc_Variance(data , X_)
    S = no_grouped.Calc_Standart_Variation(S_2)
    CV_Percent = no_grouped.Calc_Coefficient_Variation(S , X_)

    return {
            "Base_Results": {
                "n" : n,
            },
            "Frecuences_Results": {
                'xi': Arr_xi,
                'fi': Arr_fi,
                'Fi': Arr_Fi,
                'hi': Arr_hi,
                'Hi': Arr_Hi,
                'pi': Arr_pi,
                'Pi': Arr_Pi,
            },
            "Centray_Tendency_Measures": {
                'X_': X_,
                'Me': Me,
                'Mo': Mo,
            },
            "Dispersion_Measures": {
                "S_2" : S_2,
                "S" : S,
                "CV%" : CV_Percent,
            },
        }

def read_data_from_excel(file_path, column_name):
    df = pd.read_excel(file_path)

    return df[column_name].dropna().tolist()

def gestionar_datos(file_path, column_name , type_variable , precision):

    # Leer los datos desde Excel
    data = read_data_from_excel(file_path , column_name)
    print(data[::50])
    results = {}

    if not data:
        raise Exception("No se encontraron datos para realizar los calculos.")

    n = len(data)

    if type_variable == "Discreta":
        results = Get_Results_For_Not_Grouped_Data(data)
        return results
    elif type_variable == "Continua":
        m = 1 + (3.322*np.log10(n))
        if(m >= 5):
            results = Get_Results_For_Grouped_Data(data)
            return results
        else:
            results = Get_Results_For_Not_Grouped_Data(data)
            return results
    else:
        raise  Exception("No se ha seleccionado el tipo de variable.")
    
if(__name__ == "__main__"):
    """
        ==================================================================
        Este bloque de codigo solo se usa para pruebas y Debugging.
        ==================================================================
    """
    Excel_Path = filedialog.askopenfilenames(filetypes=[("Archivos Excel" , "*.xlsx")])
    if(Excel_Path):
        Excel = pd.read_excel(Excel_Path[0] , engine="openpyxl" , nrows=3)
        columns_list = [coln for coln in Excel.columns.tolist()]
        print(columns_list)
        column_name = input("Ingrese el nombre de la columna: ")
        while(not column_name in columns_list):
            print("Valor invalido, intente nuevamente")
            column_name = input("Ingrese el nombre de la columna: ")

        variable = ["Discreta" , "Continua"]
        variable_type = int(input("Ingrese el tipo de variable (1 = Discreta ; 2 = Continua): "))
        while(variable_type > 2 or variable_type < 1):
            print("Valor invalido, intente nuevamente")
            variable_type = int(input("Ingrese el tipo de variable (1 = Discreta ; 2 = Continua): "))

        precision = int(input("Ingrese la precsion de los resultados: "))
        results = gestionar_datos(Excel_Path[0] , column_name , variable[variable_type - 1] , precision)

        for name , val in results.items():
            print("\n")
            print(f"{name} : {val}")

        print(results)