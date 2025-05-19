import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from excception_handler import WarningException

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from imports import cache

def Extract_Columns_Name_From_Excel(Excel_Route , Columns_Name , Sheet_Number):
    Excel = pd.ExcelFile(Excel_Route , engine='openpyxl')

    Sheet_Names = Excel.sheet_names
    if(Sheet_Number.get() > len(Sheet_Names)):
        Sheet_Number.set(Sheet_Number.get() - 1)
        raise WarningException("El numero de hoja seleccionado no existel")

    Sheet_To_Read_Data = Sheet_Names[Sheet_Number.get() - 1]

    Excel = pd.read_excel(Excel_Route, sheet_name=Sheet_To_Read_Data , engine='openpyxl', dtype=str , nrows=3) # Lee todas las columnas del Excel como str y revisa solo las primeras 3 filas
    print(Excel)
    Excel.columns = Excel.columns.str.strip() # Elimina espacios en los nombres " Name " => "Name"
    Excel = Excel.map(lambda x: x.strip() if isinstance(x, str) else x) # Elimina espacios en blanco dentro de los valores de cada columna

    if Excel.empty:
        raise WarningException("Error", "El archivo se encuentra vacio")

    Columns_With_Data = Excel.columns[~Excel.isnull().all()] # Elimina las columnas sin ningun dato

    Valid_Columns = [val for val in Columns_With_Data if pd.notna(val) and not "Unnamed" in str(val)] # Elimina las columnas sin un encabezado valido
    print(Valid_Columns)

    if(not Valid_Columns):
        raise WarningException("No se encontraron columnas con nombres validos.")

    if(Columns_Name):
        Columns_Name.clear()

    for val in Valid_Columns:
        Columns_Name.append(val) # Almacena los nombres de las columnas para ser mostradas en la ventana principal.

    return Excel

def Change_Sheet_In_Loaded_Excel(Path_Excel , Columns_Name , Input_Columns_Name , Sheet_Number):
    try:
        Extract_Columns_Name_From_Excel(Path_Excel.get() , Columns_Name , Sheet_Number)

        Input_Columns_Name["values"] = Columns_Name
        Input_Columns_Name.set(Columns_Name[0])

    except Exception as e:
        messagebox.showerror("Error", f"{e}")
    except WarningException as e:
        messagebox.showwarning("Advertencia" , f"{e}")

def Load_Excel(Path_Excel , Columns_Name , Input_Columns_Name , Sheet_Number):
    try:
        Excel_Route = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])

        if Excel_Route:
            Path_Excel.set(Excel_Route)
            Excel = Extract_Columns_Name_From_Excel(Excel_Route , Columns_Name , Sheet_Number)

            Input_Columns_Name["values"] = Columns_Name
            Input_Columns_Name.set(Columns_Name[0])

            if Excel is not None:
                cache.agregar_archivo_reciente(Excel_Route)

    except Exception as e:
        messagebox.showerror("Error", f"{e}")
    except WarningException as e:
        messagebox.showwarning("Advertencia" , f"{e}")

def mostrar_recientes(frame_padre, Path_Excel , Columns_Name , Input_Columns_Name , Sheet_Number):
    try:
        for widget in frame_padre.winfo_children():
            widget.destroy()

        Paths_In_Cache = cache.obtener_archivos_recientes()
        if Paths_In_Cache:
            for Path_In_Cache in Paths_In_Cache:
                nombre = os.path.basename(Path_In_Cache)
                btn = tk.Button(frame_padre, text=nombre, width=25, anchor='w', command=lambda: seleccionar_archivo(Path_In_Cache , Path_Excel , Columns_Name , Input_Columns_Name , Sheet_Number))
                btn.pack(fill='x', padx=2, pady=2)
        else:
            lbl = tk.Label(frame_padre, text="No hay archivos recientes", bg='white')
            lbl.pack()
    except Exception as e:
        messagebox.showerror("Error" , f"{e}")

def seleccionar_archivo(Path_In_Cache, Path_Excel , Columns_Name , Input_Columns_Name , Sheet_Number):
    Path_Excel.set(Path_In_Cache)
    Extract_Columns_Name_From_Excel(Path_In_Cache , Columns_Name , Sheet_Number)

    Input_Columns_Name["values"] = Columns_Name
    Input_Columns_Name.set(Columns_Name[0])