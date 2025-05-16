import ttkbootstrap as ttkb
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaProcesamiento:
    tabla_contador = 1  # contador de tablas
    grafico_contador = 1  # contador de gráficos

    def __init__(self):
        self.root = ttkb.Window(themename="flatly")
        self.root.title("Procesamiento de Datos")
        self.root.iconbitmap("assets/icono.ico")
        self.root.configure(bg="#F5ECD5", highlightthickness=0, bd=0) 

        width, height = 1000, 900
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.contenedor = tk.Frame(self.root, bg="#F5ECD5", highlightthickness=0, bd=0)
        self.contenedor.pack(padx=20, pady=20, fill="both", expand=True)

        self.mostrar_tabla_frecuencia()

        self.root.mainloop()

    def mostrar_tabla_frecuencia(self):
        # === Aquí podrían reemplazar por el DataFrame procesado desde sus datos ===
        df_frecuencia = pd.DataFrame({
            "Clase": [],
            "Frecuencia": [],
        })

        # Calcular columnas adicionales (frecuencia acumulada, relativa, etc.)
        df_frecuencia["Frec. Acumulada"] = df_frecuencia["Frecuencia"].cumsum()
        df_frecuencia["Frec. Relativa"] = (df_frecuencia["Frecuencia"] / df_frecuencia["Frecuencia"].sum()).round(2)
        df_frecuencia["Frec. Rel. Acum."] = (df_frecuencia["Frec. Acumulada"] / df_frecuencia["Frecuencia"].sum()).round(2)
        df_frecuencia["Pi%"] = ((df_frecuencia["Frecuencia"] / df_frecuencia["Frecuencia"].sum()) * 100).round(2)
        df_frecuencia["Pi Acum."] = df_frecuencia["Pi%"].cumsum().round(2)

        # Agregar fila total al final
        total_row = {
            "Clase": "Total",
            "Frecuencia": df_frecuencia["Frecuencia"].sum(),
            "Frec. Acumulada": "",
            "Frec. Relativa": df_frecuencia["Frec. Relativa"].sum().round(2),
            "Frec. Rel. Acum.": "",
            "Pi%": df_frecuencia["Pi%"].sum().round(2),
            "Pi Acum.": ""
        }

        df_frecuencia = pd.concat([df_frecuencia, pd.DataFrame([total_row])], ignore_index=True)

        if not df_frecuencia.empty:
            columnas = list(df_frecuencia.columns)
            filas_totales = len(df_frecuencia)

            # Título y subtítulo de la tabla
            titulo = tk.Label(self.contenedor, text=f"Tabla {self.tabla_contador:02d}: Frecuencia de la variable",
                              font=("Segoe UI", 12, "bold"), bg="#F5ECD5")
            titulo.pack(pady=(10, 5))

            subtitulo = tk.Label(self.contenedor, text="Distribución de frecuencias agrupadas por intervalos",
                                 font=("Segoe UI", 10), bg="#F5ECD5")
            subtitulo.pack(pady=(0, 10))

            # Estilo de tabla con ttkbootstrap y colores personalizados
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Custom.Treeview", background="#FFFFFF", foreground="black", fieldbackground="#F5ECD5",
                            rowheight=25, font=("Segoe UI", 10))
            style.configure("Custom.Treeview.Heading", background="#5D6D7E", foreground="white",
                            font=("Segoe UI", 10, "bold"))
            style.map("Custom.Treeview", background=[("selected", "#2C3E50")], foreground=[("selected", "white")])

            # Frame contenedor de la tabla sin bordes adicionales
            tabla_frame = tk.Frame(self.contenedor, bg="#F5ECD5", highlightthickness=0, bd=0)
            tabla_frame.pack(pady=(0, 5), fill="both", expand=True)

            tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                                 height=filas_totales, style="Custom.Treeview")

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, anchor="center", width=130)

            tabla.tag_configure("oddrow", background="#FFFFFF")
            tabla.tag_configure("evenrow", background="#E6E6E6")

            for index, fila in df_frecuencia.iterrows():
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                tabla.insert("", tk.END, values=tuple(fila), tags=(tag,))

            tabla.pack(fill="both", expand=True)

            # Pie de tabla
            pie = tk.Label(self.contenedor, text="Fuente: Datos generados automáticamente.",
                           font=("Segoe UI", 8, "italic"), bg="#F5ECD5")
            pie.pack(pady=(0, 15))

            # Llamar al gráfico
            self.mostrar_grafico(df_frecuencia[df_frecuencia["Clase"] != "Total"])  # Excluir fila total

            VentanaProcesamiento.tabla_contador += 1

    def mostrar_grafico(self, df_frecuencia):
        # Crear gráfico con Matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_frecuencia["Clase"], df_frecuencia["Frecuencia"], color="#5D6D7E")
        ax.set_title(f"Gráfico {self.grafico_contador:02d}: Distribución de Frecuencias", fontsize=14, fontweight="bold")
        ax.set_xlabel("Clases", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)

        # Agregar porcentajes dentro de las barras
        for i, v in enumerate(df_frecuencia["Frecuencia"]):
            ax.text(i, v + 1, f'{df_frecuencia["Pi%"].iloc[i]:.2f}%', ha='center', fontsize=10)

        # Pie de gráfico
        plt.figtext(0.5, -0.05, "Fuente: Datos generados automáticamente.", ha="center", fontsize=8, style='italic')

        # Frame contenedor del gráfico
        grafico_frame = tk.Frame(self.contenedor, bg="#F5ECD5", highlightthickness=0, bd=0)
        grafico_frame.pack(pady=(10, 0), fill="both", expand=True)

        # Insertar el gráfico en el Frame 
        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.get_tk_widget().config(bg="#F5ECD5", highlightthickness=0, bd=0)

        VentanaProcesamiento.grafico_contador += 1

