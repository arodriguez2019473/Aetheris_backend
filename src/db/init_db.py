import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from db.conexion import get_conexion 

def crear_tabla_usuarios():
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()

crear_tabla_usuarios()
print("Tabla usuarios creada con éxito! 💥")

