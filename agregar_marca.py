from flask import Flask, jsonify
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json

app = Flask(__name__)

# Obtener las credenciales de la variable de entorno
google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not google_credentials_json:
    print("❌ ERROR: No se encontraron las credenciales de Google en las variables de entorno.")
    exit(1)

# Guardar las credenciales en un archivo temporal
credenciales_path = "/tmp/client_secrets.json"
with open(credenciales_path, "w") as cred_file:
    cred_file.write(google_credentials_json)

# Configurar la autenticación de PyDrive
gauth = GoogleAuth()
gauth.LoadClientConfigFile(credenciales_path)  # Carga la configuración de cliente

# Autenticación manual (debe hacerse al menos una vez localmente)
gauth.LocalWebserverAuth() 

# Guardar credenciales después de la autenticación
gauth.SaveCredentialsFile("/tmp/credentials.json")
drive = GoogleDrive(gauth)

# Ruta de prueba para saber si el servicio funciona
@app.route("/", methods=["GET"])
def home():
    return "🚀 API de marca de agua funcionando correctamente!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

