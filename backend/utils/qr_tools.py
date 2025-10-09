import qrcode
import io
import base64
from hashlib import sha256

def generar_qr_acceso(usuario_id: int, base_url: str = "http://localhost:8000/acceso"):
    """
    Genera un hash único y el QR codificado en base64.
    """
    qr_hash = sha256(f"{usuario_id}".encode()).hexdigest()[:16]
    qr_url = f"{base_url}/{qr_hash}"

    qr_img = qrcode.make(qr_url)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return qr_hash, qr_url, qr_base64