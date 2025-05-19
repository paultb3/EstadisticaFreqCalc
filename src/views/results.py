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
        
        self.root.state("zoomed")  # Pantalla completa

        # Canvas con scrollbar general para toda la ventana
        self.canvas = tk.Canvas(self.root, bg="#F5ECD5", highlightthickness=0)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # Frame contenedor dentro del canvas
        self.contenedor = tk.Frame(self.canvas, bg="#F5ECD5")
        self.canvas.create_window((0, 0), window=self.contenedor, anchor="nw")

        # Actualiza scrollregion cuando cambia el tamaño del contenido
        self.contenedor.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Ajustar ancho del frame al ancho del canvas para que el scroll quede pegado
        def on_canvas_configure(event):
            self.contenedor.configure(width=event.width)
        self.canvas.bind("<Configure>", on_canvas_configure)

        self.mostrar_tabla_frecuencia()
        self.regresar()
        self.root.mainloop()
        
    def estilos_personalizados(self):
        style = ttkb.Style()
        style.configure("Custom.TLabel", foreground="#222831", background="#F5ECD5", font=("Franklin Gothic Demi", 13))
        style.configure("Custom.TButton", foreground="#F5ECD5", background="#626F47", font=("Franklin Gothic Demi", 13))
        style.configure("Custom.TEntry", fieldbackground="#FFFFFF", foreground="#222831", font=("Aptos", 12))

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
            df_frecuencia = pd.DataFrame()

        if not df_frecuencia.empty:
            columnas = list(df_frecuencia.columns)

            titulo = tk.Label(self.contenedor, text=f"Tabla {self.tabla_contador:02d}: Frecuencia",
                              font=("Segoe UI", 12, "bold"), bg="#F5ECD5")
            titulo.pack(pady=(10, 5))  # reducido padding inferior

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Custom.Treeview", background="#FFFFFF", foreground="black", rowheight=25)
            style.configure("Custom.Treeview.Heading", background="#5D6D7E", foreground="white")

            tabla_frame = tk.Frame(self.contenedor, bg="#F5ECD5")
            tabla_frame.pack(fill="x")

            scroll_y = tk.Scrollbar(tabla_frame, orient="vertical")
            scroll_y.pack(side="right", fill="y")

            scroll_x = tk.Scrollbar(tabla_frame, orient="horizontal")
            scroll_x.pack(side="bottom", fill="x")

            tabla = ttk.Treeview(tabla_frame,
                                 columns=columnas,
                                 show="headings",
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set,
                                 height=8,
                                 style="Custom.Treeview")

            scroll_y.config(command=tabla.yview)
            scroll_x.config(command=tabla.xview)

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, anchor="center", width=130)

            for index, fila in df_frecuencia.iterrows():
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                tabla.insert("", tk.END, values=tuple(fila), tags=(tag,))

            tabla.pack(fill="both", expand=True)

            # Mostrar gráfico inmediatamente después sin espacio extra
            self.mostrar_grafico(df_frecuencia)

    def mostrar_grafico(self, df_frecuencia):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(df_frecuencia["Clase"], df_frecuencia["Frecuencia"], color="#5D6D7E")
        ax.set_title(f"Gráfico {self.grafico_contador:02d}: Distribución de Frecuencias", fontsize=14, fontweight="bold")
        ax.set_xlabel("Clases", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)

        for i, v in enumerate(df_frecuencia["Frecuencia"]):
            ax.text(i, v + 0.5, f'{df_frecuencia["Pi%"].iloc[i]:.2f}%', ha='center', fontsize=10)

        plt.tight_layout()

        grafico_frame = tk.Frame(self.contenedor, bg="#F5ECD5")
        grafico_frame.pack(fill="x", expand=True, padx=20, pady=10)  # Agrega margen horizontal y separador vertical

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)  # Esta línea es clave para evitar el espacio en blanco

        # Llamar a la función de la tabla de resultados estadísticos después de mostrar el gráfico
        self.mostrar_resultados_estadisticos()

    def mostrar_resultados_estadisticos(self):
        # Título de la tabla primero, antes de la tabla
        titulo = tk.Label(self.contenedor, text=f"Tabla {self.tabla_contador + 1:02d}: Medidas Estadísticas",
                        font=("Segoe UI", 12, "bold"), bg="#F5ECD5")
        titulo.pack(pady=(20, 5))  # Asegúrate de que el título sea el primero en el pack

        # Frame para la tabla
        frame_tabla = tk.Frame(self.contenedor, bg="#F5ECD5")
        frame_tabla.pack(pady=5)

        # Estilo ya definido previamente en mostrar_tabla_frecuencia()
        tabla = ttk.Treeview(frame_tabla, columns=("Medida", "Valor"), show="headings", height=8, style="Custom.Treeview")

        tabla.heading("Medida", text="Medida")
        tabla.heading("Valor", text="Valor")
        tabla.column("Medida", anchor="center", width=180)
        tabla.column("Valor", anchor="center", width=140)

        # Preparar datos
        medidas = [
            ("Media", f"{self.data['media']:.2f}"),
            ("Mediana", f"{self.data['mediana']:.2f}"),
            ("Moda", ", ".join(map(str, self.data['moda'])) if isinstance(self.data['moda'], list) else str(self.data['moda'])),
            ("Varianza", f"{self.data['varianza']:.2f}"),
            ("Desviación Estándar", f"{self.data['desviacion']:.2f}"),
            ("Coef. de Variación", f"{self.data['coef_variacion']:.2f}%")
        ]

        for i, (medida, valor) in enumerate(medidas):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tabla.insert("", tk.END, values=(medida, valor), tags=(tag,))

        # Empaquetar la tabla de manera controlada para que esté debajo del gráfico
        tabla.pack(pady=(20, 10))  # Espaciado adicional si lo deseas entre el gráfico y la tabla

    def regresar(self):
        btn_regresar = ttkb.Button(self.contenedor, text="🔄 Volver a calcular", style="Custom.TButton", command=self.ir_a_main)
        btn_regresar.place(x=1180, y=900)


    def ir_a_main(self):
        from views.main import mainWindow
        self.root.withdraw()
        app = mainWindow()
