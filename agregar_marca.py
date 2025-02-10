from flask import Flask, jsonify
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json

app = Flask(__name__)

# Obtener las credenciales desde la variable de entorno en Render
google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not google_credentials_json:
    print("❌ ERROR: No se encontraron las credenciales de Google en las variables de entorno.")
    exit(1)

# Guardar las credenciales en un archivo temporal
credenciales_path = "/tmp/client_secrets.json"
with open(credenciales_path, "w") as cred_file:
    cred_file.write(google_credentials_json)

# Configurar la autenticación con Google Drive sin navegador
gauth = GoogleAuth()
gauth.LoadClientConfigFile(credenciales_path)

# Cargar credenciales desde el archivo si existen
credenciales_guardadas = "/tmp/credentials.json"
if os.path.exists(credenciales_guardadas):
    gauth.LoadCredentialsFile(credenciales_guardadas)

# Si las credenciales están vencidas o no existen, autenticamos con Refresh
if gauth.credentials is None or gauth.access_token_expired:
    gauth.LocalWebserverAuth()  # ❌ NO USAR EN RENDER, CAMBIAMOS POR:
    gauth.CommandLineAuth()     # ✅ AUTENTICACIÓN SIN NAVEGADOR

# Guardamos credenciales para futuros accesos
gauth.SaveCredentialsFile(credenciales_guardadas)
drive = GoogleDrive(gauth)

@app.route("/", methods=["GET"])
def home():
    return "🚀 API de marca de agua funcionando correctamente!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
