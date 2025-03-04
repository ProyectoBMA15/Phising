
import random
import smtplib
import sqlite3
from twilio.rest import Client
from email.mime.text import MIMEText
# Configuración de Twilio
TWILIO_SID = "AC9ac6e0d6455d526fa5099066c8fe5f65"
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE = "+18573361847"

# Configuración de correo SMTP (Gmail en este caso)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "proyectobma15@gmail.com"
EMAIL_PASS = ""

# Base de datos SQLite
DB_NAME = "envios.db"

def init_db():
    """Creacion de la base de datos en caso no exista"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destinatario TEXT UNIQUE,
            tipo TEXT
        )
    """)
    conn.commit()
    conn.close()

def ya_enviado(destinatario):
    """Verifica si ya se envió un mensaje a la persona"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM envios WHERE destinatario = ?", (destinatario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def registrar_envio(destinatario, tipo):
    """Registra el envío en la base de datos"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO envios (destinatario, tipo) VALUES (?, ?)", (destinatario, tipo))
    conn.commit()
    conn.close()

def enviar_sms(destinatario):
    """Envía un SMS usando Twilio"""
    mensaje = "[Alerta] Se ha detectado actividad inusual en tu cuenta. Para evitar el bloqueo, verifica tu identidad aquí:"
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensaje,
        from_=TWILIO_PHONE,
        to=destinatario
    )
    print(f"SMS enviado a {destinatario}: {message.sid}")
    registrar_envio(destinatario, "SMS")

def enviar_correo(destinatario):
    """Envía un correo usando SMTP"""
    asunto = "[Simulación de Phishing] Tu cuenta de Facebook ha sido bloqueada"
    mensaje = "Hemos detectado actividad inusual en tu cuenta de Facebook. Para proteger tu seguridad, hemos restringido temporalmente tu acceso. Para evitar la suspensión permanente, confirma tu identidad en el siguiente enlace:"
    msg = MIMEText(mensaje, "plain")
    msg["Subject"] = asunto
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, destinatario, msg.as_string())

    print(f"Correo enviado a {destinatario}")
    registrar_envio(destinatario, "Correo")

def cargar_destinatarios(nombre_archivo):
    """Lee los destinatarios desde un archivo .txt"""
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as file:
            destinatarios = [line.strip() for line in file.readlines() if line.strip()]
        print("Destinatarios cargados:",destinatarios)
        return destinatarios
    except FileNotFoundError:
        print("Error: No se encontró el archivo de destinatarios.")
        return []
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo de destinatarios.")
        return []

def enviar_mensajes(destinatarios):
    """Decide si enviar un SMS o correo a cada destinatario"""
    for destinatario in destinatarios:
        if ya_enviado(destinatario):
            print(f"{destinatario} ya recibió un mensaje. Se omite el envío.")
            continue

        if "@" in destinatario:
            enviar_correo(destinatario)
        else:
            enviar_sms(destinatario)

if __name__ == "__main__":
    init_db()
    destinatarios = cargar_destinatarios("destinatarios.txt")
    if destinatarios:
        enviar_mensajes(destinatarios)
    else:
        print("No hay destinatarios para enviar mensajes.")