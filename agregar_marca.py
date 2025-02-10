from flask import Flask, request, jsonify
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json

app = Flask(__name__)

# Cargar credenciales desde una variable de entorno en Render
google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not google_credentials_json:
    print("❌ ERROR: No se encontraron las credenciales de Google en las variables de entorno.")
    exit(1)  # Termina la ejecución si no hay credenciales

# Guardar las credenciales en un archivo temporal para PyDrive
credenciales_path = "/tmp/credentials.json"  # Ruta temporal en el servidor
with open(credenciales_path, "w") as cred_file:
    cred_file.write(google_credentials_json)

# Autenticación con Google Drive
gauth = GoogleAuth()
gauth.LoadCredentialsFile(credenciales_path)  # Cargar credenciales desde el archivo

if gauth.credentials is None:
    print("❌ ERROR: No se pudo cargar las credenciales correctamente.")
    exit(1)
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile(credenciales_path)  # Guardar credenciales para evitar login repetido
drive = GoogleDrive(gauth)

# ID de las carpetas en Google Drive
carpeta_entrada_id = "1kz0A-9fYZ6kXKtJubjXBYb7OjQnePZ2m"  # Reemplaza con tu carpeta de entrada
carpeta_salida_id = "1k6OuxdkS5SHPJo1LoqEjK9-zwog7Zeui"  # Reemplaza con tu carpeta de salida

# Ruta de prueba para saber si el servicio funciona
@app.route("/", methods=["GET"])
def home():
    return "🚀 API de marca de agua funcionando correctamente!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
