import os 
import json

ruta_archivo = 'usuarios.json'

def cargar_usuarios():
    
    if not os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'w') as f:
            json.dump([], f)

    with open(ruta_archivo, 'r') as f:
        return json.load(f)

def guardar_usuarios(lista):
    
    with open(ruta_archivo, 'w') as f:
        json.dump(lista, f, indent=2)