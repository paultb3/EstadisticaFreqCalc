import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , '..')))

from src.excception_handler import WarningException
from calcs import cualitative_data as Freq_Cualitative_Data
from calcs import cuantitative_grouped_data as Freq__Cuantitative_Grouped_Data
from calcs import cuantitative_no_grouped_data as Freq_Cuantitative_No_Grouped_Data

def Check_Type_Of_Data(Data_List):
    Is_Cuantitative = True
    try:
        for data in Data_List:
            int(data)
    except ValueError:
        Is_Cuantitative = False

    if(Is_Cuantitative):
        Is_Cuantitative_Continue = any([True if "." in str(val) else False for val in Data_List])

    return Is_Cuantitative , Is_Cuantitative_Continue

def Convert_str_Input_To_List(Data_Entered):
    Value = ""
    Data = []
    Spacers = [" " , "\n" , "," , ";" , "\t"]
    for n in range(0,len(Data_Entered)):
        char = Data_Entered[n]
        if(char in Spacers or n==len(Data_Entered)-1):
            """ Primero se comprueba que no haya un salto en blanco o un salto de linea o si la cadena esta a punto de terminar"""
            if(n==len(Data_Entered)-1 and not char in Spacers):
                """ Si la cadena esta por terminar, se añade el ultimo caracter para no quedar incompleta"""
                Value+=char

            if(Value==""):
                """ Si el valor que estamos armando no tiene nada, pasa a la siguiente iteracion """
                continue

            else:
                """ Si hay algo entonces se añade a todos los datos y se devuelve a su valor inicial """
                Data.append(Value)
                Value = ""
        else:
            Value += char

    return Data

def Get_Results_From_Cuantitative_Grouped_Data(Data_List , Precision):
    n = len(Data_List)





def Principal_Function(Data_Entered):
    Data_List = Convert_str_Input_To_List(Data_Entered)
    Is_Cuantitative , Is_Cuantitative_Continue = Check_Type_Of_Data(Data_List)

    match(Is_Cuantitative):
        case True:
            if(Is_Cuantitative_Continue):
                pass
            else:
                pass
        case False:
            pass