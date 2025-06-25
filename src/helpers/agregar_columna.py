import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.db.conexion import get_conexion

conexion = get_conexion()
cursor = conexion.cursor()

cursor.execute("ALTER TABLE usuarios ADD COLUMN contraseña TEXT;")

conexion.commit()
conexion.close()

print("Columna 'contraseña' añadida con éxito 🛡️")
