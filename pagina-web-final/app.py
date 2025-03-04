from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar flask-cors

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Tu lógica para procesar el login
    return jsonify({"success": True, "message": "Login successful"})

if __name__ == "__main__":
    app.run(debug=True)