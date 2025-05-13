import sys
import os
import pandas as pd

# Agrega al path las rutas de los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importa tus módulos personalizados
import cuantitative_grouped_data as grouped
import cuantitative_no_grouped_data as no_grouped

# =================== FUNCIONES DE GESTIÓN ===================

def detectar_tipo_dato(data):
    """
    Detecta si los datos son cuantitativos continuos o discretos.
    """
    es_discreto = all(float(x).is_integer() for x in data)
    return "Discreto" if es_discreto else "Continuo"

def gestionar_datos(file_path, column_name):
    try:
        # Leer los datos desde Excel
        df = pd.read_excel(file_path)
        data = df[column_name].dropna().tolist()

        if not data:
            print(f">>> La columna '{column_name}' está vacía o no existe en el archivo.")
            return

        tipo_dato = detectar_tipo_dato(data)
        cantidad_datos = len(data)

        print(f"\n>>> Tipo de dato detectado: {tipo_dato}")
        print(f">>> Cantidad de datos: {cantidad_datos}")

        if cantidad_datos <= 50:
            print("\n>>> Procesando datos NO AGRUPADOS...\n")
            no_grouped.read_data_from_excel(file_path, column_name)
        else:
            print("\n>>> Procesando datos AGRUPADOS...\n")
            grouped.read_data_from_excel(file_path, column_name)

    except FileNotFoundError:
        print(">>> Archivo no encontrado. Verifica la ruta.")
    except KeyError:
        print(f">>> La columna '{column_name}' no fue encontrada en el archivo.")
    except Exception as e:
        print(f">>> Error inesperado: {e}")
