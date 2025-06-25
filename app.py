import os

from flask import Flask
from flask_cors import CORS
# from src.auth.auth import auth_bp
from src.usuario.user import usuario_bp
from src.tablas.regitroFacturas import registro_bp

app = Flask(__name__)
CORS(app)

# app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(registro_bp, url_prefix='/registroFacturas')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)