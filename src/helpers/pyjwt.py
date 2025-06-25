import jwt
import datetime

SECRET_KEY = "mi_clave_secreta"

def crear_token(usuario):
    payload = {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "es_admin": usuario["es_admin"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expira en 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
