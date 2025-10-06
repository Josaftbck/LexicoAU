import base64
from io import BytesIO
from PIL import Image

def redimensionar_imagen_base64(imagen_b64: str, size=(300, 300)) -> str:
    try:
        # Decodificar la imagen base64 a bytes
        imagen_bytes = base64.b64decode(imagen_b64)

        # Convertir a objeto PIL
        imagen = Image.open(BytesIO(imagen_bytes))

        # Convertir a RGB si es necesario (algunas vienen en modo RGBA o L)
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')

        # Redimensionar la imagen con antialiasing para mantener calidad
        imagen.thumbnail(size, Image.LANCZOS)

        # Guardar en buffer
        buffer = BytesIO()
        imagen.save(buffer, format="JPEG", quality=80)  # También puede ser PNG si prefieres
        imagen_redimensionada_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return imagen_redimensionada_b64

    except Exception as e:
        print("Error redimensionando imagen:", e)
        return imagen_b64  # en caso de error, devolver la imagen original sin tocar