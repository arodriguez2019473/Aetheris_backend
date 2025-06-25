from flask import Blueprint, request, jsonify
from src.db.conexion import get_pg_conn      

usuario_bp = Blueprint('usuario', __name__)

MSG_FALTA_DATOS = {"mensaje": "falta de datos"}
MSG_USUARIO_NO_ENCONTRADO = {"mensaje": "usuario no encontrado"}
MSG_USUARIO_CREADO = "El usuario a sido creado"
MSG_USUARIO_ACTUALIZADO = "Usuario actualizado correctamente"
MSG_USUARIO_ELIMINADO = "Usuario eliminado correctamente"

# nuevas consultas SQL para postgres
SQL_INSERT      = "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s) RETURNING id"
SQL_SELECT_ALL  = "SELECT id, nombre, edad FROM usuarios"
SQL_SELECT_BY_ID= "SELECT id, nombre, edad FROM usuarios WHERE id = %s"
SQL_UPDATE      = "UPDATE usuarios SET nombre=%s, edad=%s WHERE id=%s"
SQL_DELETE      = "DELETE FROM usuarios WHERE id=%s"

def get_db_cursor():
    conexion = get_pg_conn()
    cursor = conexion.cursor()
    return conexion, cursor

@usuario_bp.route('/', methods=['POST'])
def post_usuario():
    data = request.json
    nombre = data.get('nombre')
    edad = data.get('edad')

    if not nombre or not edad:
        return jsonify(MSG_FALTA_DATOS), 400

    conexion, cursor = get_db_cursor()
    cursor.execute(SQL_INSERT, (nombre, edad))
    conexion.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": MSG_USUARIO_CREADO,
        "usuario": {"id": user_id, "nombre": nombre, "edad": edad}
    }), 201

@usuario_bp.route('/', methods=['GET'])
def get_usuario():
    conexion, cursor = get_db_cursor()
    cursor.execute(SQL_SELECT_ALL)
    usuarios = cursor.fetchall()
    lista_usuarios = [
        {'id': u[0], 'nombre': u[1], 'edad': u[2]} for u in usuarios
    ]
    cursor.close()
    conexion.close()
    return jsonify(lista_usuarios)

@usuario_bp.route('/<int:id>', methods=['GET'])
def get_usuario_por_id(id):
    conexion, cursor = get_db_cursor()
    cursor.execute(SQL_SELECT_BY_ID, (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not usuario:
        return jsonify(MSG_USUARIO_NO_ENCONTRADO), 404

    usuario_dict = {'id': usuario[0], 'nombre': usuario[1], 'edad': usuario[2]}
    return jsonify(usuario_dict)

@usuario_bp.route('/<int:id>', methods=['PUT'])
def put_usuario(id):
    data = request.json
    nombre = data.get('nombre')
    edad = data.get('edad')

    if not nombre or not edad:
        return jsonify(MSG_FALTA_DATOS), 400

    conexion, cursor = get_db_cursor()
    cursor.execute(SQL_UPDATE, (nombre, edad, id))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()

    if filas_afectadas == 0:
        return jsonify(MSG_USUARIO_NO_ENCONTRADO), 404

    return jsonify({"mensaje": MSG_USUARIO_ACTUALIZADO}), 200

@usuario_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    conexion, cursor = get_db_cursor()
    cursor.execute(SQL_DELETE, (id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()

    if filas_afectadas == 0:
        return jsonify(MSG_USUARIO_NO_ENCONTRADO), 404

    return jsonify({"mensaje": MSG_USUARIO_ELIMINADO}), 202
