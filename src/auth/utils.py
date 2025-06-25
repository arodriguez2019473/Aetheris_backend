from passlib.hash import pbkdf2_sha256

def hash_contraseña(contraseña):
    return pbkdf2_sha256.hash(contraseña)

def verificar_contraseña(contraseña, hash_guardado):
    return pbkdf2_sha256.verify(contraseña, hash_guardado)