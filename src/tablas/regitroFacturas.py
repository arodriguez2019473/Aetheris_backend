# src/tablas/registroFacturas.py   ← mismo nombre, nuevo contenido
from flask import Blueprint, request, jsonify
from psycopg2 import sql          # para construir UPDATE dinámico sin inyección
from src.db.conexion import get_pg_conn   # ← usa tu función que retorna psycopg2.connect

registro_bp = Blueprint('registro', __name__)

# ---------- helpers ----------
def get_db_cursor():
    conn = get_pg_conn()
    cur = conn.cursor()
    return conn, cur

# campos fijos
CAMPOS_OBLIG = [
    "nombre_factura", "fecha_factura", "tipo_factura",
    "total_factura", "envio", "metodo_pago", "estado"
]
CAMPOS_TODOS = CAMPOS_OBLIG + [
    "vendedor", "cantidad_producto", "precio_producto",
    "id_factura", "direccion_factura"
]

# ---------- endpoints ----------
@registro_bp.route('/', methods=['POST'])
def registrar_datos():
    data = request.json or {}

    faltantes = [c for c in CAMPOS_OBLIG if not data.get(c)]
    if faltantes:
        return jsonify({"mensaje": f"Faltan datos obligatorios: {', '.join(faltantes)}"}), 400

    # prepara tuplas de columnas y valores (mantén orden)
    cols   = []
    values = []
    for campo in CAMPOS_TODOS:
        if campo in data and data[campo] is not None:
            cols.append(sql.Identifier(campo))
            values.append(data[campo])

    query = sql.SQL("INSERT INTO registro_datos ({}) VALUES ({}) RETURNING id") \
              .format(
                  sql.SQL(", ").join(cols),
                  sql.SQL(", ").join(sql.Placeholder() * len(values))
              )

    try:
        conn, cur = get_db_cursor()
        cur.execute(query, values)
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"mensaje": "El registro ha sido creado",
                        "registro": {**data, "id": new_id}}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al registrar los datos", "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ------------------------------
@registro_bp.route('/', methods=['GET'])
def listar_facturas():
    try:
        conn, cur = get_db_cursor()
        cur.execute("SELECT * FROM registro_datos")
        colnames = [d[0] for d in cur.description]
        rows = [dict(zip(colnames, r)) for r in cur.fetchall()]
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener facturas", "error": str(e)}), 500
    finally:
        cur.close(); conn.close()

# ------------------------------
@registro_bp.route('/<int:factura_id>', methods=['GET'])
def obtener_factura(factura_id):
    try:
        conn, cur = get_db_cursor()
        cur.execute("SELECT * FROM registro_datos WHERE id = %s", (factura_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"mensaje": "Factura no encontrada"}), 404
        factura = dict(zip([d[0] for d in cur.description], row))
        return jsonify(factura), 200
    except Exception as e:
        return jsonify({"mensaje": "Error al obtener factura", "error": str(e)}), 500
    finally:
        cur.close(); conn.close()

# ------------------------------
@registro_bp.route('/<int:factura_id>', methods=['PUT'])
def actualizar_factura(factura_id):
    data = request.json or {}
    # filtra solo campos válidos presentes
    pares = {k: v for k, v in data.items() if k in CAMPOS_TODOS}

    if not pares:
        return jsonify({"mensaje": "No se enviaron datos para actualizar"}), 400

    # construye SET dinámico seguro
    set_clause = sql.SQL(", ").join(
        sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder()])
        for k in pares.keys()
    )
    values = list(pares.values()) + [factura_id]

    try:
        conn, cur = get_db_cursor()
        cur.execute(
            sql.SQL("UPDATE registro_datos SET {} WHERE id = %s").format(set_clause),
            values
        )
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"mensaje": "Factura no encontrada"}), 404
        return jsonify({"mensaje": "Factura actualizada correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al actualizar factura", "error": str(e)}), 500
    finally:
        cur.close(); conn.close()

# ------------------------------
@registro_bp.route('/<int:factura_id>', methods=['DELETE'])
def eliminar_factura(factura_id):
    try:
        conn, cur = get_db_cursor()
        cur.execute("DELETE FROM registro_datos WHERE id = %s", (factura_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"mensaje": "Factura no encontrada"}), 404
        return jsonify({"mensaje": "Factura eliminada correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": "Error al eliminar factura", "error": str(e)}), 500
    finally:
        cur.close(); conn.close()
