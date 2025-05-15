import pandas as pd
import numpy as np
import os
import math

from decimal import Decimal
# =================== FUNCIONES ===================

def find_min(data):
    return np.min(data)

def find_max(data):
    return np.max(data)

def find_range(data):
    return np.max(data) - np.min(data)

def log_n(n):
    return math.log10(n)

def calculate_m(n):
    return 1 + (3.322 * log_n(n))

def round_m(m, ):
    return round(m)

def calculate_amplitude(rango, m_redondeado , max_n_decimals_in_data):
    """
        ==============================================================================================
        Esta funcion se encarga de redondear la amplitud, recibe un valor y le añade una decima de mas 
        para que el ultimo intervalo se pase un poco del valor maximo del dataset.
        Ejemplos de uso:
            Input: 1.3456 , N_Decimals = 2
            Output: 1.346

            Input: 0.02 , N_Decimals = 2
            Output: 0.021
        ==============================================================================================
    """
    Number = rango/m_redondeado
    N_Decimals = max_n_decimals_in_data
    if(Number - round(Number) != 0):
        """ print(f"{Number=}") """
        Integer_Part = str(Number).split(".")[0]
        Decimal_Part = str(Number).split(".")[1]

        N_Decimals = N_Decimals if N_Decimals < len(Decimal_Part) else len(Decimal_Part)
        if(N_Decimals > len(Decimal_Part) - 1):
            Decimal_Part += "0"
    
        if(int(Decimal_Part[N_Decimals]) >= 5):
            Decimal_Part = "".join([val for i , val in enumerate(Decimal_Part , start=1) if i <= N_Decimals])
            Value_To_Add = float("0." + "0"*(N_Decimals - 1) + "1")
        else:
            Decimal_Part = "".join([val for i , val in enumerate(Decimal_Part , start=1) if i <= N_Decimals + 1])
            Value_To_Add = "0." + "0"*N_Decimals + "1"
            N_Decimals += 1

        Number = float(Integer_Part + "." + Decimal_Part)
        
        """ print("Numero cortado: " , Number) """

        Decimals_To_Round = "1." + "0"*(N_Decimals) if N_Decimals > 0 else "1"

        Number = float(Decimal(str(Number)).quantize(Decimal(Decimals_To_Round)))
        
        Number += float(Value_To_Add)
        """ print(f"{Number=}") """

        return round(Number , N_Decimals) , N_Decimals
    else:
        return Number + 0.1

def calc_intervals(vmin, amplitud, m , N_Decimals_C):
    intervals = []
    lower = vmin
    for _ in range(m):
        upper = lower + amplitud
        upper = round(upper , N_Decimals_C)
        intervals.append([lower, upper])
        lower = upper
    return intervals

def calc_fi(data, intervals):
    fi = []
    for lower, upper in intervals:
        count = sum(1 for x in data if lower <= x < upper)
        fi.append(count)
    return fi

def calc_fi_cumulative(fi):
    return np.cumsum(fi)

def calc_hi(fi, n):
    return [f / n for f in fi]

def calc_hi_cumulative(hi):
    return np.cumsum(hi)

def calc_pi_percent(hi):
    return [h * 100 for h in hi]

def calc_pi_cumulative(pi):
    return np.cumsum(pi)

def calc_midpoints(intervals):
    return [(l + u) / 2 for l, u in intervals]

def calc_mean(midpoints, fi, n):
    return sum([f * x for f, x in zip(fi, midpoints)]) / n

def calc_median(intervals, fi, n, amplitud):
    Fi = calc_fi_cumulative(fi)
    median_class_idx = next(i for i, F in enumerate(Fi) if F >= n / 2)
    L = intervals[median_class_idx][0]
    F_prev = Fi[median_class_idx - 1] if median_class_idx > 0 else 0
    f = fi[median_class_idx]
    return L + ((n / 2 - F_prev) / f) * amplitud

def calc_mode(intervals, fi, amplitud):
    modal_idx = np.argmax(fi)
    L = intervals[modal_idx][0]
    f1 = fi[modal_idx]
    f0 = fi[modal_idx - 1] if modal_idx > 0 else 0
    f2 = fi[modal_idx + 1] if modal_idx + 1 < len(fi) else 0
    if (2*f1 - f0 - f2) == 0:
        return L
    return L + ((f1 - f0) / (2*f1 - f0 - f2)) * amplitud

if(__name__ == "__main__"):
    print(calculate_amplitude(1363 , 7 , 2))
