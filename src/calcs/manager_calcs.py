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
    vmin = grouped.Find_Min(data)
    vmax = grouped.Find_Max(data)
    rango = grouped.Calc_Range(data)
    m = grouped.Calc_Intervals_Number(n)
    m_redondeado = grouped.Calc_Rounded_Intervals_Number(m)

    max_n_decimals_in_data = Find_Max_Decimal_Number_In_Dataset(data)

    amplitud = rango / m_redondeado
    amplitud_redondeada , N_Decimals_C = grouped.Calc_Amplitude(rango, m_redondeado , max_n_decimals_in_data)

    intervals = grouped.Calc_Intervals(vmin, amplitud, m_redondeado , N_Decimals_C)

    midpoints = grouped.Calc_xi(intervals)

    fi = grouped.Calc_fi(data, intervals)
    fi_cum = grouped.Calc_Fi(fi)

    hi = grouped.Calc_hi(fi, n)
    hi_cum = grouped.Calc_Hi(hi)

    pi = grouped.Calc_pi(hi)
    pi_cum = grouped.Calc_Pi(pi)

    mean = grouped.Calc_Aithmetic_Average(midpoints , fi , n)
    median = grouped.Calc_Median(intervals , fi , n , amplitud , fi)
    mode = grouped.Calc_Mode(intervals, amplitud , fi)

    S_2 = grouped.Calc_Variance(midpoints , fi , mean , n)
    S = grouped.Calc_Standart_Variation(S_2)
    CV_Percent = grouped.Calc_Coefficient_Variation(S , mean)

    Arr_Quartiles = grouped.Calc_Quantile(intervals , fi_cum , n , amplitud_redondeada , fi , "Cuartil")
    Arr_Deciles = grouped.Calc_Quantile(intervals , fi_cum , n , amplitud_redondeada , fi , "Decil")
    Arr_Percentiles = grouped.Calc_Quantile(intervals , fi_cum , n , amplitud_redondeada , fi , "Percentil")

    # Retornar todos los resultados en un diccionario
    return {
            "Base_Results": {
                'vmin': vmin,
                'vmax': vmax,
                'rango': rango,
                'n': n,
                'm': m,
                'm_redondeado': m_redondeado,
                'amplitud': amplitud,
                'amplitud_redondeada': amplitud_redondeada,
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
            "Central_Tendency_Measures":{
                'X_': mean,
                'Me': median,
                'Mo': mode,
            },
            "Position_Measures":{
                'Cuartiles': Arr_Quartiles,
                'Deciles': Arr_Deciles,
                'Percentiles': Arr_Percentiles,
            },
            "Dispersion_Measures":{
                "S_2": S_2,
                "S": S,
                "CV%": CV_Percent,
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
            "Central_Tendency_Measures": {
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

def gestionar_datos(file_path, column_name , type_variable):

    # Leer los datos desde Excel
    data = read_data_from_excel(file_path , column_name)
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

def Print_Results_Grouped_Data_In_Terminal(results , precision):
    for name , values in results.items():
        if(name == "Frecuences_Results"):
            print(f"{name:=^149}")
            space = 18
            space_fi_Fi = 10
            space_intervals = 30
            frecuence = list(values.keys())
                
            print(f"|{frecuence[0]:^{space_intervals}}|{frecuence[1]:^{space}}|{frecuence[2]:^{space_fi_Fi}}|{frecuence[3]:^{space_fi_Fi}}|{frecuence[4]:^{space}}|{frecuence[5]:^{space}}|{frecuence[6]:^{space}}|{frecuence[7]:^{space}}|")
            print(f"|{'':-^{space_intervals}}|{'':-^{space}}|{'':-^{space_fi_Fi}}|{'':-^{space_fi_Fi}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            intervals_text = [f"[ {Limit[0]} - {Limit[1]} >" for Limit in values["intervalos"]]
                
            for idx in range(0 , len(intervals_text)):
                pi_text = f"{values["pi"][idx]:.{precision}f}%"
                Pi_text = f"{values["Pi"][idx]:.{precision}f}%"
                print(f"|{intervals_text[idx]:^{space_intervals}}|{values["xi"][idx]:^{space}.{precision}f}|{values["fi"][idx]:^{space_fi_Fi}}|{values["Fi"][idx]:^{space_fi_Fi}}|{values["hi"][idx]:^{space}.{precision}f}|{values["Hi"][idx]:^{space}.{precision}f}|{pi_text:^{space}}|{Pi_text:^{space}}|")
            print(f"|{'':-^{space_intervals}}|{'':-^{space}}|{'':-^{space_fi_Fi}}|{'':-^{space_fi_Fi}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            print(f"|{'Total':^{space_intervals}}|{'':^{space}}|{np.sum(values["fi"]):^{space_fi_Fi}}|{'':^{space_fi_Fi}}|{round(np.sum(values["hi"]) , 3):^{space}}|{'':^{space}}|{f'{round(np.sum(values["pi"]) , 3)}%':^{space}}|{'':^{space}}|")
            print(f"{'':=^149}")
        elif(name == "Central_Tendency_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_central_tendency_measure = list(values.keys())

            print(f"|{name_central_tendency_measure[0]:^{space}}|{name_central_tendency_measure[1]:^{space}}|{name_central_tendency_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            if(len(values["Mo"]) > 1):
                print(f"|{values["X_"]:^{space}.{precision}f}|{values["Me"]:^{space}.{precision}f}|{values["Mo"][0]:^{space}.{precision}f}|")
                for i , Mo in enumerate(values["Mo"]):
                    if(i == 0):
                        continue
                    print(f"|{'':^{space}}|{'':^{space}}|{Mo:^{space}.{precision}f}|")
            else:
                print(f"|{values["X_"]:^{space}.{precision}f}|{values["Me"]:^{space}.{precision}f}|{values["Mo"][0]:^{space}.{precision}f}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Dispersion_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_dispersion_measure = list(values.keys())

            print(f"|{name_dispersion_measure[0]:^{space}}|{name_dispersion_measure[1]:^{space}}|{name_dispersion_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            print(f"|{values["S_2"]:^{space}.{precision}f}|{values["S"]:^{space}.{precision}f}|{values["CV%"]:^{space}.{precision}f}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Position_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_position_measure = list(values.keys())

            print(f"|{name_position_measure[0]:^{space}}|{name_position_measure[1]:^{space}}|{name_position_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            for i in range(0 , 20):
                if(i < 3):
                    Quartiles_Text = f"Q_{i + 1}: {values["Cuartiles"][i]:.{precision}f}"
                    Deciles_Text = f"D_{i + 1}: {values["Deciles"][i]:.{precision}f}"
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{Quartiles_Text:^{space}}|{Deciles_Text:^{space}}|{Percentiles_Text:^{space}}|")
                elif(i < 9):
                    Deciles_Text = f"D_{i + 1}: {values["Deciles"][i]:.{precision}f}"
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{'':^{space}}|{Deciles_Text:^{space}}|{Percentiles_Text:^{space}}|")
                else:
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{'':^{space}}|{'':^{space}}|{Percentiles_Text:^{space}}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Base_Results"):
            space = 50
            print(f"{name:=^{space + 2}}")
            for name_b_result , value in values.items():
                print(f"|{name_b_result:^{space}}|")
                print(f"|{'':-^{space}}|")
                print(f"|{value:^{space}}|")
                print(f"|{'':_^{space}}|")
            print(f"{'':=^{space + 2}}")
        print("\n")

def Print_Results_No_Grouped_Data_In_Terminal(results , precision):
    for name , values in results.items():
        if(name == "Frecuences_Results"):
            print(f"{name:=^149}")
            space = 22
            space_xi = 25
            space_fi_Fi = 14
            frecuence = list(values.keys())
                
            print(f"|{frecuence[0]:^{space_xi}}|{frecuence[1]:^{space_fi_Fi}}|{frecuence[2]:^{space_fi_Fi}}|{frecuence[3]:^{space}}|{frecuence[4]:^{space}}|{frecuence[5]:^{space}}|{frecuence[6]:^{space}}|")
            print(f"|{'':-^{space_xi}}|{'':-^{space_fi_Fi}}|{'':-^{space_fi_Fi}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
                
            for idx in range(0 , len(values["xi"])):
                pi_text = f"{values["pi"][idx]:.{precision}f}%"
                Pi_text = f"{values["Pi"][idx]:.{precision}f}%"
                print(f"|{values["xi"][idx]:^{space_xi}}|{values["fi"][idx]:^{space_fi_Fi}}|{values["Fi"][idx]:^{space_fi_Fi}}|{values["hi"][idx]:^{space}.{precision}f}|{values["Hi"][idx]:^{space}.{precision}f}|{pi_text:^{space}}|{Pi_text:^{space}}|")
            print(f"|{'':-^{space_xi}}|{'':-^{space_fi_Fi}}|{'':-^{space_fi_Fi}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            print(f"|{'Total':^{space_xi}}|{np.sum(values["fi"]):^{space_fi_Fi}}|{'':^{space_fi_Fi}}|{round(np.sum(values["hi"]) , 3):^{space}}|{'':^{space}}|{f'{round(np.sum(values["pi"]) , 3)}%':^{space}}|{'':^{space}}|")
            print(f"{'':=^149}")
        elif(name == "Central_Tendency_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_central_tendency_measure = list(values.keys())

            print(f"|{name_central_tendency_measure[0]:^{space}}|{name_central_tendency_measure[1]:^{space}}|{name_central_tendency_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            if(len(values["Mo"]) > 1):
                print(f"|{values["X_"]:^{space}.{precision}f}|{values["Me"]:^{space}.{precision}f}|{values["Mo"][0]:^{space}.{precision}f}|")
                for i , Mo in enumerate(values["Mo"]):
                    if(i == 0):
                        continue
                    print(f"|{'':^{space}}|{'':^{space}}|{Mo:^{space}.{precision}f}|")
            else:
                print(f"|{values["X_"]:^{space}.{precision}f}|{values["Me"]:^{space}.{precision}f}|{values["Mo"][0]:^{space}.{precision}f}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Dispersion_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_dispersion_measure = list(values.keys())

            print(f"|{name_dispersion_measure[0]:^{space}}|{name_dispersion_measure[1]:^{space}}|{name_dispersion_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            print(f"|{values["S_2"]:^{space}.{precision}f}|{values["S"]:^{space}.{precision}f}|{values["CV%"]:^{space}.{precision}f}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Position_Measures"):
            space = 40
            print(f"{name:=^{(space*3) + 4}}")
            name_position_measure = list(values.keys())

            print(f"|{name_position_measure[0]:^{space}}|{name_position_measure[1]:^{space}}|{name_position_measure[2]:^{space}}|")
            print(f"|{'':-^{space}}|{'':-^{space}}|{'':-^{space}}|")
            for i in range(0 , 20):
                if(i < 3):
                    Quartiles_Text = f"Q_{i + 1}: {values["Cuartiles"][i]:.{precision}f}"
                    Deciles_Text = f"D_{i + 1}: {values["Deciles"][i]:.{precision}f}"
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{Quartiles_Text:^{space}}|{Deciles_Text:^{space}}|{Percentiles_Text:^{space}}|")
                elif(i < 9):
                    Deciles_Text = f"D_{i + 1}: {values["Deciles"][i]:.{precision}f}"
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{'':^{space}}|{Deciles_Text:^{space}}|{Percentiles_Text:^{space}}|")
                else:
                    Percentiles_Text = f"P_{i + 1}: {values["Percentiles"][i]:.{precision}f}"
                    print(f"|{'':^{space}}|{'':^{space}}|{Percentiles_Text:^{space}}|")
            print(f"{'':=^{(space*3) + 4}}")
        elif(name == "Base_Results"):
            space = 50
            print(f"{name:=^{space + 2}}")
            for name_b_result , value in values.items():
                print(f"|{name_b_result:^{space}}|")
                print(f"|{'':-^{space}}|")
                print(f"|{value:^{space}}|")
                print(f"|{'':_^{space}}|")
            print(f"{'':=^{space + 2}}")
        print("\n")

def Clear_Terminal():
    os.system('cls' if os.name == "nt" else 'clear')

if(__name__ == "__main__"):
    """
        ==================================================================
        Este bloque de codigo solo se usa para pruebas y Debugging.
        ==================================================================
    """
    Stop = False
    while(not Stop):
        Excel_Path = filedialog.askopenfilenames(filetypes=[("Archivos Excel" , "*.xlsx")])
        if(Excel_Path):
            Excel = pd.read_excel(Excel_Path[0] , engine="openpyxl" , nrows=3)
            columns_list = [coln for coln in Excel.columns.tolist()]
            for i , col_name in enumerate(columns_list):
                print(f"{i + 1}. {col_name}")
            
            column_index = int(input("Ingrese el numero de la columna a importar: "))
            while(column_index < 0 or column_index > len(columns_list)):
                Clear_Terminal()
                for i , col_name in enumerate(columns_list):
                    print(f"{i + 1}. {col_name}")
                print("Valor invalido, intente nuevamente")
                column_index = int(input("Ingrese el nombre de la columna: "))
            Clear_Terminal()

            variable = ["Discreta" , "Continua"]
            variable_type = int(input("Ingrese el tipo de variable (1 = Discreta ; 2 = Continua): "))
            while(variable_type > 2 or variable_type < 1):
                Clear_Terminal()

                print("Valor invalido, intente nuevamente")
                variable_type = int(input("Ingrese el tipo de variable (1 = Discreta ; 2 = Continua): "))
            Clear_Terminal()

            precision = int(input("Ingrese la precsion de los resultados (1 - 10): "))
            while(precision < 1 or precision > 11):
                Clear_Terminal()

                print("Valor invalido, intente nuevamente")
                precision = int(input("Ingrese la precsion de los resultados (1 - 10): "))
            Clear_Terminal()

            results = gestionar_datos(Excel_Path[0] , columns_list[column_index - 1] , variable[variable_type - 1])
            if(variable_type == 1):
                Print_Results_No_Grouped_Data_In_Terminal(results , precision)
            elif(variable_type == 2):
                Print_Results_Grouped_Data_In_Terminal(results , precision)

            print("\n")

            # Descargar graficos
            """ Download_Graphs = input("Deseea descargar los graficos (s/n): ")
            while(Download_Graphs.lower() != "s" and Download_Graphs.lower() != "n"):
                Clear_Terminal()

                print("Opcion Invalida, intente nuevamente")
                Download_Graphs = input("Deseea descargar los graficos (s/n): ")

            match(Download_Graphs.lower()):
                case "s":
                    pass
                case "n":
                    pass """

            Continue = input("Deseea realizar otro calculo (s/n): ")
            while(Continue.lower() != "s" and Continue.lower() != "n"):
                Clear_Terminal()

                print("Opcion Invalida, intente nuevamente")
                Continue = input("Deseea realizar otro calculo (s/n): ")
            
            match(Continue.lower()):
                case "s":
                    pass
                case "n":
                    Stop = True