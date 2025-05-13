import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from path_manager import Get_Resource_Path
from excception_handler import WarningException
from tkinter import *
from tkinter import messagebox

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
from views.results import VentanaProcesamiento


class mainWindow:
    def __init__(self):
        self.root = ttkb.Window(themename="flatly")
        self.root.title("TabuladorPy")
        self.root.iconbitmap("assets/icono.ico")
        width, height = 700, 550

        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.configure(bg="#F5ECD5")

        self.estilos_personalizados()

        self.crear_botones()
        self.crear_entradas()
        self.texto()

    def estilos_personalizados(self):
        style = ttkb.Style()

        style.configure("Custom.TLabel", foreground="#222831", background="#F5ECD5", font=("Franklin Gothic Demi", 13))
        style.configure("Custom.TButton", foreground="#F5ECD5", background="#626F47", font=("Franklin Gothic Demi", 13), borderwidth=0, focusthickness=3, focuscolor='none')
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#222831", font=("Aptos", 12))

    def texto(self):
        label_ingresarExcel = ttkb.Label(self.root, text="Cargue la tabla de excel:", style="Custom.TLabel")
        label_ingresarExcel.place(x=110, y=30)

        label_nombreColumna = ttkb.Label(self.root, text="Nombre de la columna:", style="Custom.TLabel")
        label_nombreColumna.place(x=110, y=130)

        entry_nombreColumna = ttkb.Entry(self.root, style="Custom.TEntry", width=58)
        entry_nombreColumna.place(x=110, y=170)
        
        label_nombreFila = ttkb.Label(self.root, text="Nombre de la fila:", style="Custom.TLabel")
        label_nombreFila.place(x=110, y=215)

        entry_nombreFila = ttkb.Entry(self.root, style="Custom.TEntry", width=58)
        entry_nombreFila.place(x=110, y=250)
        
        label_tipoVariable = ttkb.Label(self.root, text="Tipo de variable:", style="Custom.TLabel")
        label_tipoVariable.place(x=110, y=295)

        label_presicion = ttkb.Label(self.root, text="Presición:", style="Custom.TLabel")
        label_presicion.place(x=110, y=390)

    def crear_botones(self):
        iconoExcel_pil = Image.open("assets/icono-excel.png").resize((24, 24), Image.LANCZOS)
        self.iconoExcel = ImageTk.PhotoImage(iconoExcel_pil)
        
        btncargarexcel = ttkb.Button(self.root, image=self.iconoExcel, compound=LEFT, text="Cargar Excel", style="Custom.TButton")
        btncargarexcel.place(x=110, y=70)

        btnprocesar = ttkb.Button(self.root, text="Procesar", style="Custom.TButton", command=self.abrir_ventana_procesamiento)
        btnprocesar.place(x=300, y=470)

    def crear_entradas(self):
        spinbox_numerico = ttkb.Spinbox(self.root, from_=0, to=100, font=("Aptos", 10), width=10)
        spinbox_numerico.place(x=110, y=430)

        opciones = ["Discreta", "Continua"]
        seleccion = ttkb.Combobox(self.root, values=opciones, state="readonly", font=("Franklin Gothic Demi", 12), width=22)
        seleccion.set("Seleccionar tipo de variable")
        seleccion.place(x=110, y=330)

    def run(self):
        self.root.mainloop()
        
    def abrir_ventana_procesamiento(self):
        self.root.destroy()  # Cierra la ventana actual
        VentanaProcesamiento() 

    def Process_Data(self):
        try:
            self.Validate_Data()
            Dictionary_Results = manager_calcs.Principal_Function(self.Data_From_Widget_Entry.get() , self.Decimals_Precision.get())
        except WarningException as e:
            messagebox.showwarning("Advertencia" , f"{e}")
        except Exception as e:
            messagebox.showerror("Error" , f"{e}")

    def Validate_Data(self):
        if(not self.Data_From_Widget_Entry.get()):
            raise WarningException("No se han ingresado datos.")
        if(self.Decimals_Precision < 0):
            raise WarningException("Valor no valido para la precision.")

if __name__ == "__main__":
    app = mainWindow()
    app.run()
