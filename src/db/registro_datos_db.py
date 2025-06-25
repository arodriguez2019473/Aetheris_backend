import sys
import os
from datetime import datetime
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from db.conexion import registro_datos

def crear_tabla_facturas():
    conexion = registro_datos()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreFactura TEXT NOT NULL,
            fechaFactura TEXT NOT NULL,
            totalFactura REAL NOT NULL,
            tipoFactura TEXT NOT NULL,
            vendedor TEXT,
            cantidadProducto INTEGER,
            precioProducto REAL,
            idFactura TEXT,
            envio TEXT NOT NULL,
            direccionFactura TEXT,
            metodoPago TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexion.commit()
    conexion.close()
    print("✅ Tabla 'registro_datos' creada con éxito")

crear_tabla_facturas()
