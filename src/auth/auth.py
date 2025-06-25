from flask import Blueprint, request, jsonify
from src.db.conexion import get_conexion
from src.auth.utils import hash_contraseña, verificar_contraseña

auth_bp = Blueprint('auth',__name__, url_prefix='/auth')

@auth_bp.route('/registro', methods=['POST'])

def registrar_usuario():

    data = request.json

    nombre = data.get('nombre')
    contraseña = data.get('contraseña')

    if not nombre or not contraseña:
        return jsonify({"mensaje":"nos falta datos"}), 400
    
    
    hash_pwd = hash_contraseña(contraseña)
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO usuario (nombre, contraseña) VALUES (?, ?)",(nombre,hash_pwd))
    conexion.commit()
    conexion.close()

    return jsonify({"mensaje":"El usuario a sido registrado"}), 201

@auth_bp.route('/login', methods=['POST'])

def login():

    data = request.json
    
    nombre = data.get('nombre')
    contraseña =  data.get('contraseña')

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
    
    usuario = cursor.fetchone()
    conexion.close()

    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    if verificar_contraseña(contraseña,usuario["contraseña"]):
        return jsonify({"mensaje": f"Bienvenido pa, {nombre}"}),200

    else:
        return jsonify({"mensaje": "contraseña incorrecta"})
        