import pandas as pd
from tkinter import filedialog
from collections import Counter

def Import_Data_From_Excel(Excel_Path , Column_Name):
    """ 
        ===============================================
        El codigo de abajo servira para seleccionar y
        validar el numero de hoja del excel
        ===============================================
    """
    """ 
    sheet_number = 0

    Prev_Load_Excel = pd.ExcelFile(Excel_Path , engine="openpyxl")

    Sheet_Names = Prev_Load_Excel.sheet_names
    Sheet_Name = Sheet_Names[sheet_number]
    print(Sheet_Name)
    """
    Excel = pd.read_excel(Excel_Path , engine="openpyxl")

    Columns_In_Excel = Excel.columns.tolist()
    print(Columns_In_Excel)
    if(not Column_Name in Columns_In_Excel):
        raise Exception("No existe la columna especificada")

    Imported_Data = Excel[Column_Name]

    Imported_Data.dropna()
    Imported_Data.values
    
    Array_With_Data = [val for val in Imported_Data.tolist()]
    Array_With_Data = Array_With_Data

    Arr = Counter(Array_With_Data)
    Arr_xi = [xi for xi in Arr.keys()]
    Arr_fi = [fi for fi in Arr.values()]

    print(Arr_xi)
    print(Arr_fi)

if __name__ == "__main__":
    Excel_Path = filedialog.askopenfilenames(title="Seleccione el archivo Excel" , filetypes=[("Archivos Excel" , "*.xlsx")])
    print(Excel_Path[0])
    Import_Data_From_Excel(Excel_Path[0] , "numero_hijos")