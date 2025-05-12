import ttkbootstrap as ttkb

class VentanaProcesamiento:
    def __init__(self):
        self.root = ttkb.Window(themename="flatly")
        self.root.title("Procesamiento de Datos")
        self.root.iconbitmap("assets/icono.ico")
        self.root.configure(bg="#F5ECD5")
        width, height = 900, 700
        
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        label = ttkb.Label(self.root, text="Aquí va el procesamiento", font=("Franklin Gothic Demi", 16), background="#F5ECD5")
        label.pack(pady=50)

        self.root.mainloop()