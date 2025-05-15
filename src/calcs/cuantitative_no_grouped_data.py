import pandas as pd
import numpy as np

import statistics

# =================== Calculo de Frecuencias ===================
def Calc_fi_and_xi(data):
    Arr_xi = list(set(data))
    Arr_xi.sort()

    Arr_fi = []
    for xi in Arr_xi:
        Arr_fi.append(data.count(xi))
    return Arr_xi , Arr_fi

def Calc_Fi(Arr_fi):
    return np.cumsum(Arr_fi)

def Calc_hi(Arr_fi , n):
    return [fi / n for fi in Arr_fi]

def Calc_Hi(Arr_hi):
    return np.cumsum(Arr_hi)

def Calc_pi_percent(Arr_hi):
    return [hi * 100 for hi in Arr_hi]

def Calc_Pi_percent(Arr_pi):
    return [pi * 100 for pi in Arr_pi]

# ========================================================= Medidas de Tendencia Central =========================================================
def Calc_Atihmetic_Average(data):
    return np.sum(data) / len(data)

def Calc_Median(data):
    return statistics.median(data)

def Calc_Mode_Mo(Arr_xi , Arr_fi):
    Max_Rep = max(Arr_fi)
    Mo = [Arr_xi[a] for a in range(0 , len(Arr_fi)) if Arr_fi[a] == Max_Rep]
    if(len(Mo) == len(Arr_xi)):
        return "Amodal"

    return Mo

# ========================================================= Medidas de Posicion =========================================================
def Calc_Quartil(data):
    pass
def Calc_Decile(data):
    pass
def Calc_Percentile(data):
    pass

# ========================================================= Medidas de Dispercion =========================================================

def Calc_Variance(data , Arithmetic_Average):
    return np.sum((xi - Arithmetic_Average)**2 for xi in data)/(len(data) - 1)

def Calc_Standart_Variation(S_2):
    return np.sqrt(S_2)

def Calc_Coefficient_Variation(S , Arithmetic_Average):
    return (S/Arithmetic_Average) * 100

