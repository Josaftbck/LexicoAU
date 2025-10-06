from PIL import Image, ImageDraw, ImageFont
import qrcode
import random
import string
import os

def generar_qr(codigo_texto, nombre_archivo):
    qr = qrcode.make(codigo_texto)
    qr.save(nombre_archivo)

def generar_credencial(nombre, usuario, correo, ruta_foto="foto_usuario.jpg", plantilla="plantilla_credencial.png"):
    carpeta_salida = "credenciales"
    os.makedirs(carpeta_salida, exist_ok=True)

    # 1. Generar código QR aleatorio
    codigo_qr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    ruta_qr = os.path.join(carpeta_salida, f"{usuario}_qr.png")
    generar_qr(codigo_qr, ruta_qr)

    # 2. Cargar plantilla
    fondo = Image.open(plantilla).convert("RGBA")
    draw = ImageDraw.Draw(fondo)

    # 3. Fuente
    try:
        fuente = ImageFont.truetype("DejaVuSans-Bold.ttf", size=28)
    except:
        fuente = ImageFont.load_default()

    # 4. Dibujar texto en mejor posición
    draw.text((360, 120), f"Nombre: {nombre}", font=fuente, fill="black")
    draw.text((360, 170), f"Usuario: {usuario}", font=fuente, fill="black")
    draw.text((360, 220), f"Email: {correo}", font=fuente, fill="black")

    # 5. Insertar foto centrada en su cuadro
    cuadro_foto = (60, 250, 260, 500)  # (x1, y1, x2, y2)
    foto = Image.open(ruta_foto).resize((160, 160))
    x_foto = cuadro_foto[0] + ((cuadro_foto[2] - cuadro_foto[0] - 160) // 2)
    y_foto = cuadro_foto[1] + ((cuadro_foto[3] - cuadro_foto[1] - 160) // 2)
    fondo.paste(foto, (x_foto, y_foto))

    # 6. Insertar QR centrado en su cuadro
    cuadro_qr = (900, 450, 1100, 600)
    qr_img = Image.open(ruta_qr).resize((140, 140))
    x_qr = cuadro_qr[0] + ((cuadro_qr[2] - cuadro_qr[0] - 140) // 2)
    y_qr = cuadro_qr[1] + ((cuadro_qr[3] - cuadro_qr[1] - 140) // 2)
    fondo.paste(qr_img, (x_qr, y_qr))

    # 7. Guardar credencial
    ruta_final = os.path.join(carpeta_salida, f"{usuario}_credencial.png")
    fondo.save(ruta_final)
    print(f"✅ Credencial generada en: {ruta_final}")

# ==== EJECUCIÓN ====
if __name__ == "__main__":
    print("🪪 Generador de Credenciales — DEMO")
    nombre = input("Nombre completo: ")
    usuario = input("Nombre de usuario: ")
    correo = input("Correo electrónico: ")
    generar_credencial(nombre, usuario, correo)