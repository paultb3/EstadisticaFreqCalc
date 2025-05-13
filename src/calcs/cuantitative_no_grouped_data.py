import pandas as pd
import numpy as np
import statistics
from collections import Counter

# Leer los datos desde un archivo Excel
def read_data_from_excel(file_path, column_name):
    df = pd.read_excel(file_path)
    data = df[column_name].dropna().tolist()
    
    # Verificar si todos los valores son enteros
    es_discreto = all(float(x).is_integer() for x in data)

    tipo_dato = "Discreto" if es_discreto else "Continuo"
    print(f"\n>>> Tipo de datos detectado en '{column_name}': {tipo_dato}")

    return data

# Calcular las estadísticas básicas
def calcular_estadisticas(data):
    n = len(data)
    minimo = min(data)
    maximo = max(data)
    rango = maximo - minimo
    media = sum(data) / n
    mediana = statistics.median(data)
    
    try:
        moda = statistics.mode(data)
    except statistics.StatisticsError:
        moda = "No hay una sola moda"
    
    desviacion_std = statistics.stdev(data)

    return {
        "Cantidad de datos": n,
        "Valor mínimo": minimo,
        "Valor máximo": maximo,
        "Rango": rango,
        "Media": media,
        "Mediana": mediana,
        "Moda": moda,
        "Desviación estándar": desviacion_std
    }

# Calcular la tabla de frecuencias similar a datos agrupados
def calcular_tabla_frecuencias(data):
    # Contar las frecuencias de cada valor
    freq = Counter(data)
    
    # Total de datos
    n = len(data)
    
    # Calcular frecuencias acumuladas
    fi_acumulada = np.cumsum(list(freq.values())).tolist()
    
    # Calcular frecuencias relativas
    hi = [f / n for f in freq.values()]
    
    # Calcular frecuencias relativas acumuladas
    Hi = np.cumsum(hi).tolist()
    
    # Calcular porcentajes relativos
    pi = [h * 100 for h in hi]
    
    # Calcular porcentajes acumulados
    Pi = np.cumsum(pi).tolist()

    # Preparar los valores para la tabla
    valores = list(freq.keys())
    frecuencias = list(freq.values())
    
    # Generar la tabla
    tabla = {
        'Valor': valores,
        'fi': frecuencias,
        'Fi': fi_acumulada,
        'hi': hi,
        'Hi': Hi,
        '%hi': pi,
        '%Hi': Pi
    }
    
    return tabla

