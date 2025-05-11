
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from imports import cache

def importar_excel_seguro(archivo):
    try:
        datos = pd.read_excel(archivo, engine='openpyxl', dtype=str)
        datos.columns = datos.columns.str.strip()
        datos = datos.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        if datos.empty:
            messagebox.showerror("Error", "El archivo está vacío")
            return None

        columnas_vacias = datos.columns[datos.isnull().all()]
        if not columnas_vacias.empty:
            aviso = f"Advertencia: Las siguientes columnas están completamente vacías:\n{', '.join(columnas_vacias)}"
            messagebox.showwarning("Advertencia", aviso)

        info = f"Archivo cargado correctamente\nFilas: {datos.shape[0]} | Columnas: {datos.shape[1]}\n\n"
        info += "Columnas: " + ", ".join(datos.columns[:5])
        if datos.shape[1] > 5:
            info += ", ..."
        messagebox.showinfo("Resumen", info)

        return datos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
        return None

def cargar_excel(entry_widget):
    archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    if archivo:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, archivo)
        datos = importar_excel_seguro(archivo)
        if datos is not None:
            cache.agregar_archivo_reciente(archivo)

def mostrar_recientes(frame_padre, entry_widget):
    
    for widget in frame_padre.winfo_children():
        widget.destroy()

    archivos = cache.obtener_archivos_recientes()
    if archivos:
        for archivo in archivos:
            nombre = os.path.basename(archivo)
            btn = tk.Button(frame_padre, text=nombre, width=25, anchor='w',
                            command=lambda a=archivo: seleccionar_archivo(a, entry_widget))
            btn.pack(fill='x', padx=2, pady=2)
    else:
        lbl = tk.Label(frame_padre, text="No hay archivos recientes", bg='white')
        lbl.pack()

def seleccionar_archivo(archivo, entry_widget):
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, archivo)
    importar_excel_seguro(archivo)
