# backend/utils/qr_utils.py

import qrcode
import base64
import hashlib
import io
from datetime import datetime

def generar_qr_unico(usuario_id: int, base_url: str = "http://localhost:8000/acceso"):
    """
    Genera un código QR único para un usuario y devuelve:
    - qr_base64: imagen QR en base64
    - qr_hash: hash SHA256 del contenido
    - qr_contenido: texto real que codifica el QR (URL única)
    """
    # 🔹 Crear contenido único (URL + timestamp)
    raw_content = f"{base_url}/user/{usuario_id}?t={datetime.utcnow().timestamp()}"

    # 🔹 Generar hash seguro (para validación en login QR)
    qr_hash = hashlib.sha256(raw_content.encode()).hexdigest()

    # 🔹 Crear imagen QR
    qr_img = qrcode.make(raw_content)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")

    # 🔹 Convertir a Base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "qr_base64": qr_base64,
        "qr_hash": qr_hash,
        "qr_contenido": raw_content
    }