from PIL import Image
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Configuración de carpetas
carpeta_entrada = "imagenes/"  # Carpeta donde están las imágenes originales
carpeta_salida = "procesadas/"  # Carpeta donde se guardarán las imágenes con la marca de agua

# Asegurar que la carpeta de salida exista
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Agregar marca de agua a cada imagen
def agregar_marca_de_agua(imagen_path, salida_path):
    # Abrir la imagen original
    imagen = Image.open(imagen_path).convert("RGBA")
    ancho, alto = imagen.size

    # Cargar la imagen de la marca de agua
    watermark = Image.open("watermark.png")
    watermark = watermark.convert("RGBA")  # Asegúrate de que la marca de agua tenga transparencia

    # Redimensionar la marca de agua si es necesario
    watermark = watermark.resize((int(ancho / 5), int(alto / 5)))  # Redimensionar la marca de agua (ajustar según sea necesario)

    # Obtener las dimensiones de la imagen de la marca de agua
    watermark_width, watermark_height = watermark.size

    # Definir la posición donde quieres colocar la marca de agua (por ejemplo, en la esquina inferior derecha)
    posicion = (ancho - watermark_width - 10, alto - watermark_height - 10)  # Ajusta las coordenadas según lo desees

    # Añadir la marca de agua a la imagen original
    imagen.paste(watermark, posicion, watermark)  # Usa watermark como máscara para conservar la transparencia

    # Guardar la imagen con la marca de agua
    imagen.save(salida_path)
    print(f"✅ Marca de agua aplicada: {salida_path}")

# Procesar todas las imágenes en la carpeta de entrada
for archivo in os.listdir(carpeta_entrada):
    if archivo.endswith((".jpg", ".png", ".jpeg")):
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        ruta_salida = os.path.join(carpeta_salida, archivo)
        agregar_marca_de_agua(ruta_entrada, ruta_salida)

print("✅ Todas las imágenes han sido procesadas con la marca de agua.")

# ---------------------- SUBIDA A GOOGLE DRIVE ----------------------

# Autenticación con Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# ID de la carpeta de Google Drive donde quieres subir las imágenes
drive_folder_id = "1k6OuxdkS5SHPJo1LoqEjK9-zwog7Zeui"  # Reemplaza con tu carpeta de Drive

# Subir cada imagen procesada a Google Drive
for archivo in os.listdir(carpeta_salida):
    if archivo.endswith((".jpg", ".png", ".jpeg")):
        archivo_drive = drive.CreateFile({'title': archivo, 'parents': [{'id': drive_folder_id}]})
        archivo_drive.SetContentFile(os.path.join(carpeta_salida, archivo))
        archivo_drive.Upload()
        print(f"✅ Imagen subida: {archivo}")

print("🚀 ¡Todas las imágenes fueron subidas a Google Drive!")

