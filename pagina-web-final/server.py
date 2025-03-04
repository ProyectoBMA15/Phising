from flask import Flask, request, jsonify, send_file
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Importamos CORS

app = Flask(__name__)

# Habilitamos CORS para todas las rutas de la aplicación
CORS(app)

USUARIOS_FILE = 'usuarios.json'

def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    try:
        with open(USUARIOS_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {}

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as file:
        json.dump(usuarios, file, indent=4)

@app.route("/")
def home():
    return send_file("pagina principal.html")

@app.route("/registro")
def registro():
    return send_file("registro.html")

@app.route("/index")
def login():
    return send_file("index.html")

@app.route("/index-falso")
def index_falso():
    return send_file("index-falso.html")

@app.route("/pagina principal")
def pagina_principal():
    return send_file("pagina principal.html")

@app.route("/registro", methods=["POST"])
def registrar_usuario():
    datos = request.json
    usuario = datos.get('usuario')
    contrasena = datos.get('contrasena')
    
    if not usuario or not contrasena:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    
    usuarios = cargar_usuarios()
    if usuario in usuarios:
        return jsonify({'error': 'El usuario ya existe'}), 400
    
    usuarios[usuario] = generate_password_hash(contrasena)
    guardar_usuarios(usuarios)
    
    return jsonify({'mensaje': 'Usuario registrado con éxito'}), 201

@app.route("/login", methods=["POST"])
def iniciar_sesion():
    datos = request.json
    usuario = datos.get('usuario')
    contrasena = datos.get('contrasena')
    
    usuarios = cargar_usuarios()
    
    if usuario in usuarios and check_password_hash(usuarios[usuario], contrasena):
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

@app.route("/advertencia-index.html")
def advertencia_index():
    return send_file("advertencia-index.html")

# Nueva ruta para phishing-alerta-index.html
@app.route("/phishing-alerta-index.html")
def phishing_alerta_index():
    return send_file("phishing-alerta-index.html")

if __name__ == '__main__':
    app.run(debug=True)

