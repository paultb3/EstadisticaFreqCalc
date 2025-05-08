import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from path_manager import Get_Resource_Path
from excception_handler import WarningException
from calcs import manager_calcs

from tkinter import *
from tkinter import messagebox

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
        self.Data_From_Widget_Entry = StringVar(self.Main_Window)
        self.Decimals_Precision = IntVar(self.Main_Window)

        Label_Field_For_Data = Label(self.Main_Window , text="Ingrese los datos:" , font=("Times New Roman" , 13))
        Label_Field_For_Data.place(x=20 , y=20)
        Input_Data = Entry(self.Main_Window , font=("Courier New" , 13) , textvariable=self.Data_From_Widget_Entry)
        Input_Data.place(x=150 , y=20 , width=530)

        Label_Input_Decimals_Precision = Label(self.Main_Window , text="Precision:" , font=("Times New Roman" , 13))
        Label_Input_Decimals_Precision.place(x=20 , y=60)
        Input_Decimals_Precision = Spinbox(self.Main_Window , from_=0 , to=10 , increment=1 , width=3 , font=("Courier New" , 13) , textvariable=self.Decimals_Precision)
        Input_Decimals_Precision.config(state="readonly")
        Input_Decimals_Precision.place(x=150 , y=60)

        Btn_Calc_Frecuences = Button(self.Main_Window , text="Calcular Tabla de Frecuencias" , font=("Times New Roman" , 13))
        Btn_Calc_Frecuences.place(x=230 , y=100 , width=240)

        self.Main_Window.mainloop()

    def Process_Data(self):
        try:
            self.Validate_Data()

            Results = manager_calcs.Principal_Function(self.Data_From_Widget_Entry.get() , self.Decimals_Precision.get())
            

        except WarningException as e:
            messagebox.showwarning("Advertencia" , f"{e}")
        except Exception as e:
            messagebox.showerror("Error" , f"{e}")
    def Validate_Data(self):
            if(not self.Data_From_Widget_Entry.get()):
                raise WarningException("No se han ingresado datos.")
            
            if(self.Decimals_Precision < 0):
                raise WarningException("Valor no valido para la precision.")


if(__name__ == "__main__"):
    Main = Main_Window(700 , 160 , 200 , 100 , "Calculo de Frecuencias")
    Main.Build_Window()