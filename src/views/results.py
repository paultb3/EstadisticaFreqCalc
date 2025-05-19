import ttkbootstrap as ttkb
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaProcesamiento:
    tabla_contador = 1
    grafico_contador = 1

    def __init__(self, data):
        self.data = data
        self.root = ttkb.Window(themename="flatly")
        self.root.title("Procesamiento de Datos")
        self.root.iconbitmap("assets/icono.ico")
        self.root.configure(bg="#F5ECD5", highlightthickness=0, bd=0)

        width, height = 1920, 1080
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.contenedor = tk.Frame(self.root, bg="#F5ECD5", highlightthickness=0, bd=0)
        self.contenedor.pack(padx=20, pady=20, fill="both", expand=True)

        self.mostrar_tabla_frecuencia()
        self.mostrar_resultados_estadisticos()
        self.regresar()
        self.root.mainloop()


    def mostrar_tabla_frecuencia(self):
        if self.data["tipo"] == "Discreta":
            df_frecuencia = pd.DataFrame({
                "Clase": self.data["xi"],
                "Frecuencia": self.data["fi"],
                "Frec. Relativa": self.data["hi"],
                "Frec. Rel. Acum.": self.data["Hi"],
                "Pi%": self.data["pi"],
                "Pi Acum.": self.data["Pi"]
            })
        elif self.data["tipo"] == "Continua":
            clases = [f"{i[0]} - {i[1]}" for i in self.data["intervalos"]]
            df_frecuencia = pd.DataFrame({
                "Clase": clases,
                "Frecuencia": self.data["fi"],
                "Frec. Relativa": self.data["hi"],
                "Frec. Rel. Acum.": self.data["Hi"],
                "Pi%": self.data["pi"],
                "Pi Acum.": self.data["Pi"]
            })
        else:
            df_frecuencia = pd.DataFrame()  # fallback

        # Tabla en Treeview
        if not df_frecuencia.empty:
            columnas = list(df_frecuencia.columns)
            filas_totales = len(df_frecuencia)

            titulo = tk.Label(self.contenedor, text=f"Tabla {self.tabla_contador:02d}: Frecuencia",
                              font=("Segoe UI", 12, "bold"), bg="#F5ECD5")
            titulo.pack(pady=(10, 5))

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Custom.Treeview", background="#FFFFFF", foreground="black", rowheight=25)
            style.configure("Custom.Treeview.Heading", background="#5D6D7E", foreground="white")

            tabla_frame = tk.Frame(self.contenedor, bg="#F5ECD5", highlightthickness=0)
            tabla_frame.pack(pady=(0, 5), fill="both", expand=True)

            tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=filas_totales,
                                 style="Custom.Treeview")

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, anchor="center", width=130)

            for index, fila in df_frecuencia.iterrows():
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                tabla.insert("", tk.END, values=tuple(fila), tags=(tag,))

            tabla.pack(fill="both", expand=True)

            self.mostrar_grafico(df_frecuencia)

    def mostrar_grafico(self, df_frecuencia):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_frecuencia["Clase"], df_frecuencia["Frecuencia"], color="#5D6D7E")
        ax.set_title(f"Gráfico {self.grafico_contador:02d}: Distribución de Frecuencias", fontsize=14, fontweight="bold")
        ax.set_xlabel("Clases", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)

    # Etiquetas en las barras (Pi%)
        for i, v in enumerate(df_frecuencia["Frecuencia"]):
            ax.text(i, v + 0.5, f'{df_frecuencia["Pi%"].iloc[i]:.2f}%', ha='center', fontsize=10)

        plt.tight_layout()

        grafico_frame = tk.Frame(self.contenedor, bg="#F5ECD5")
        grafico_frame.pack(pady=(10, 0), fill="both", expand=True)

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        VentanaProcesamiento.grafico_contador += 1


    def mostrar_resultados_estadisticos(self):
        marco_resultados = tk.Frame(self.contenedor, bg="#F5ECD5")
        marco_resultados.pack(pady=15, fill="x")

        titulo = tk.Label(marco_resultados, text="Medidas Estadísticas",
                          font=("Segoe UI", 12, "bold"), bg="#F5ECD5")
        titulo.pack(anchor="w")

        texto = ""
        texto += f"Media: {self.data['media']:.2f}\n"
        texto += f"Mediana: {self.data['mediana']:.2f}\n"
        if isinstance(self.data['moda'], list):
            texto += f"Moda: {', '.join(map(str, self.data['moda']))}\n"
        else:
            texto += f"Moda: {self.data['moda']}\n"
        texto += f"Varianza: {self.data['varianza']:.2f}\n"
        texto += f"Desviación Estándar: {self.data['desviacion']:.2f}\n"
        texto += f"Coef. de Variación: {self.data['coef_variacion']:.2f}%"

        label = tk.Label(marco_resultados, text=texto, justify="left",
                         font=("Segoe UI", 10), bg="#F5ECD5")
        label.pack(anchor="w")

    
    def regresar(self):
        from views.main import mainWindow  # ✅ se importa solo cuando se llama
        self.root.destroy()
        app = mainWindow()
        app.root.mainloop()

    def regresar(self):
        btn_regresar = ttkb.Button(self.contenedor, text="🔄 Volver a calcular", style="success.TButton", command=self.regresar)
        btn_regresar.pack(pady=10)
        btn_regresar.place(x=500, y=850)


