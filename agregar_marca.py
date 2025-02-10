from flask import Flask, request, jsonify, send_file
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json
from io import BytesIO

app = Flask(__name__)

# Autenticación con Google Drive
gauth = GoogleAuth()

# Cargar las credenciales desde la variable de entorno
google_credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not google_credentials_json:
    return jsonify({"error": "No se encontraron las credenciales de Google."}), 400

# Convertir el contenido JSON en un objeto de credenciales
credentials_info = json.loads(google_credentials_json)
gauth.credentials = GoogleAuth._load_credentials_from_info(credentials_info)

if gauth.credentials is None:
    gauth.LocalWebserverAuth()  # Usado solo en tu máquina local
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("credentials.json")
drive = GoogleDrive(gauth)

# ID de la carpeta de Google Drive donde están las imágenes originales y donde se subirán las procesadas
carpeta_entrada_id = "1kz0A-9fYZ6kXKtJubjXBYb7OjQnePZ2m"  # Reemplaza con el ID de la carpeta de entrada
carpeta_salida_id = "1k6OuxdkS5SHPJo1LoqEjK9-zwog7Zeui"  # Reemplaza con el ID de la carpeta de salida

# Función para aplicar la marca de agua
def agregar_marca_de_agua(imagen, salida_path):
    imagen = imagen.convert("RGBA")
    ancho, alto = imagen.size

    # Cargar la imagen de la marca de agua
    watermark = Image.open("watermark.png").convert("RGBA")
    watermark = watermark.resize((int(ancho / 5), int(alto / 5)))  # Redimensionar

    # Posición en la esquina inferior derecha
    posicion = (ancho - watermark.size[0] - 10, alto - watermark.size[1] - 10)

    # Aplicar la marca de agua
    imagen.paste(watermark, posicion, watermark)

    # Guardar en un archivo temporal
    imagen.save(salida_path)
    return salida_path

# Ruta para procesar las imágenes de la carpeta de Google Drive
@app.route("/procesar", methods=["POST"])
def procesar_imagen():
    # Buscar las imágenes en la carpeta de entrada
    file_list = drive.ListFile({'q': f"'{carpeta_entrada_id}' in parents and trashed=false"}).GetList()

    if not file_list:
        return jsonify({"error": "No se encontraron archivos en la carpeta de entrada"}), 400

    for archivo in file_list:
        print(f"Imagen encontrada: {archivo['title']}")

        # Descargar la imagen desde Google Drive
        archivo.GetContentFile(archivo['title'])

        # Abrir la imagen
        imagen = Image.open(archivo['title'])

        # Definir la ruta de salida temporal
        salida_path = f"procesadas/{archivo['title']}"

        # Aplicar la marca de agua
        agregar_marca_de_agua(imagen, salida_path)

        # Subir la imagen procesada a Google Drive
        archivo_drive = drive.CreateFile({'title': archivo['title'], 'parents': [{'id': carpeta_salida_id}]})
        archivo_drive.SetContentFile(salida_path)
        archivo_drive.Upload()

        # Eliminar el archivo temporal después de subirlo
        os.remove(salida_path)

        # Obtener la URL pública del archivo en Drive
        archivo_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        url_drive = f"https://drive.google.com/uc?id={archivo_drive['id']}"

        print(f"✅ Imagen procesada y subida con éxito: {url_drive}")

    return jsonify({"mensaje": "Todas las imágenes fueron procesadas y subidas con éxito!"})

# Ruta para verificar que la API funciona
@app.route("/", methods=["GET"])
def home():
    return "🚀 API de marca de agua funcionando correctamente!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

