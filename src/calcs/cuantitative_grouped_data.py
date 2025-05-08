import numpy as np

def Find_Max_Decimals_In_Data(Data_List):
    Decimals_Numbers = []
    for data in Data_List:
        if("." in str(data)):
            Decimals_Numbers.append(len(str(data).split(".")[1]))
        else:
            Decimals_Numbers.append(0)

    return np.max(Decimals_Numbers)

# ======================================================= Calculo de Frecuencias =======================================================

def Find_Min_Value(Data):
    return np.min(Data)

def Find_Max_Value(Data):
    return np.max(Data)

def Calc_Range(V_min , V_max):
    return V_max - V_min

def Calc_Intervals_Number(n):
    return np.round(1 + (3.322*np.log10(n)))

def Calc_Amplitude(R , m , Precision):
    if(R % m == 0):
        return R/m  #Verificar que sucede cuando la amplitud es entera
    else:
        C = R/m

        Integer_Part = str(C).split(".")[0]
        Decimal_Part = str(C).split(".")[1]
        
        if(len(Decimal_Part) > Precision):
            Decimal_Part = "".join([digit for i , digit in enumerate(Decimal_Part) if i <= Precision])

        C = float(Integer_Part + "." + Decimal_Part)
        if(int(Decimal_Part[-1]) >= 5):
            C = round(C , Precision) 
        else:
            Value_To_Add = "0." + "0"*(Precision) + "1"
            C += float(Value_To_Add)

        return C

def Calc_Intervals(m , C , V_min , V_max , Precision):
    Arr_Intervals = [[0 for _ in range(2)] for _ in range(m)]

    Acumulate = V_min
    for a in range(m):
        for b in range(2):
            if(b != 0):
                Acumulate += C
            
            Arr_Intervals[a][b] = round(Acumulate , Precision)

    return Arr_Intervals

def Calc_fi(Data , Arr_Intervals):
    Arr_fi = []
    for Limits in Arr_Intervals:
        Counter = 0
        for data in Data:
            if(Limits[0] <= data < Limits[1]):
                Counter += 1
        Arr_fi.append(Counter)

    return Arr_fi

def Calc_Fi(Arr_fi):
    return np.cumsum(Arr_fi)

def Calc_hi(Arr_fi , n):
    return [fi/n for fi in Arr_fi]

def Calc_Hi(Arr_hi):
    return np.cumsum(Arr_hi)

def Calc_pi_percent(Arr_hi):
    return [hi*100 for hi in Arr_hi]

def Calc_Pi_percent(Arr_pi):
    return np.cumsum(Arr_pi)

if __name__ == "__main__":
    print(Calc_Amplitude(90 , 5 , 5))