import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from path_manager import Get_Resource_Path
from excception_handler import WarningException
from calcs import manager_calcs

from imports.import_excel import Load_Excel , mostrar_recientes

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Main_Window():
    def __init__(self , width , height , x_pos , y_pos , title):
        self.Main_Window = Tk()
        self.Main_Window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.Main_Window.title(title)

        Icon = PhotoImage(file=Get_Resource_Path("assets/icon.png"))
        self.Main_Window.iconphoto(False , Icon)
        
        self.Main_Window.resizable(False , False)

    def Close_Window(self):
        if(self.Main_Window):
            for widget in self.Main_Window.winfo_children():
                widget.destroy()

            self.Main_Window.quit()
            self.Main_Window.destroy()

    def Build_Window(self):
        self.Path_Excel = StringVar(self.Main_Window)
        self.Decimals_Precision = IntVar(self.Main_Window)
        self.Columns_Name = []
        
        Label_Input_Archivo = Label(self.Main_Window, text="Ingrese el archivo:", font=("Times New Roman", 13))
        Label_Input_Archivo.place(x=20, y=20)

        self.Entry_Archivo = Entry(self.Main_Window, font=("Courier New", 13) , state="readonly" , textvariable=self.Path_Excel)
        self.Entry_Archivo.place(x=280, y=20, width=560)

        Btn_Recientes = Button(self.Main_Window, text="Archivos recientes", command=self.Display_Recents_Frame , font=("Times New Roman" , 13))
        Btn_Recientes.place(x=1020, y=15, width=160)

        self.Recents_Frame = Frame(self.Main_Window, bg='white', bd=1, relief='solid')
        
        self.scrollbar = Scrollbar(self.Recents_Frame, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.lista_recientes = Listbox(self.Recents_Frame, yscrollcommand=self.scrollbar.set, font=("Arial", 10))
        self.lista_recientes.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar.config(command=self.lista_recientes.yview)

        self.recientes_visibles = False

        Label_Columns_Namme = Label(self.Main_Window , text="Seleccione el nombre de la columna: " , font=("Times New Roman", 13))
        Label_Columns_Namme.place(x=20 , y=60)
        self.Input_Columns_Name = ttk.Combobox(self.Main_Window , values=self.Columns_Name , font=("Courier New" , 13))
        self.Input_Columns_Name.config(state="readonly")
        self.Input_Columns_Name.place(x=280 , y=60 , width=400)

        Btn_Cargar_Excel = Button(self.Main_Window, text="Cargar Excel", bg='green', fg='white' , font=("Times New Roman" , 13) ,  command=lambda: Load_Excel(self.Path_Excel , self.Columns_Name , self.Input_Columns_Name))
        Btn_Cargar_Excel.place(x=850, y=15, width=160)

        Label_Input_Decimals_Precision = Label(self.Main_Window, text="Precision:", font=("Times New Roman", 13))
        Label_Input_Decimals_Precision.place(x=20, y=100)

        Input_Decimals_Precision = Spinbox(self.Main_Window, from_=0, to=10, increment=1, width=3,font=("Courier New", 13), textvariable=self.Decimals_Precision)
        Input_Decimals_Precision.config(state="readonly")
        Input_Decimals_Precision.place(x=150 , y=100)

        Type_Variable = ["Cuantitativa Discreta", "Cuantitativa Continua"]

        Label_Input_Type_Variable = Label(self.Main_Window , text="Seleccione el tipo de variable:" , font=("Times New Roman" , 13))
        Label_Input_Type_Variable.place(x=300 , y=100)
        Input_Type_Variable = ttk.Combobox(self.Main_Window, values=Type_Variable, state="readonly", width=30 , font=("Times New Roman" , 13))
        Input_Type_Variable.set(Type_Variable[0])
        Input_Type_Variable.place(x=650 , y=100)

        Btn_Calc_Frecuences = Button(self.Main_Window, text="Calcular Tabla de Frecuencias", font=("Times New Roman", 13))
        Btn_Calc_Frecuences.place(x=450 , y=160 , width=300)

        self.Main_Window.mainloop()

    
    def Display_Recents_Frame(self):
        if self.recientes_visibles:
            self.Recents_Frame.place_forget()
            self.recientes_visibles = False
        else:
            mostrar_recientes(self.lista_recientes, self.Path_Excel , self.Columns_Name , self.Input_Columns_Name)
            self.Recents_Frame.place(x=1020, y=65, width=160, height=100)
            self.recientes_visibles = True

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
    Main = Main_Window(1200 , 200 , 200 , 350 , "Calculo de Frecuencias")
    Main.Build_Window()