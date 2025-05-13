# imports/cache.py
#aqui es para guardar los excel recientes ,es una idea mia 
import os
import json


CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))

RUTA_CACHE = os.path.join(CARPETA_ACTUAL, "cache")
ARCHIVO_CACHE = os.path.join(RUTA_CACHE, "archivos_recientes.json")

def crear_directorio_cache():
    if not os.path.exists(RUTA_CACHE):
        os.makedirs(RUTA_CACHE)

def cargar_cache():
    crear_directorio_cache()
    if os.path.exists(ARCHIVO_CACHE):
        with open(ARCHIVO_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_cache(archivos):
    with open(ARCHIVO_CACHE, 'w', encoding='utf-8') as f:
        json.dump(archivos, f, indent=2)

def agregar_archivo_reciente(ruta_archivo):
    archivos = cargar_cache()
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Evitar duplicados
    if ruta_archivo in archivos:
        archivos.remove(ruta_archivo)

    archivos.insert(0, ruta_archivo)  # Agrega al inicio

    # Solo se guardan los últimos 3
    archivos = archivos[:3]
    guardar_cache(archivos)

def obtener_archivos_recientes():
    return cargar_cache()
