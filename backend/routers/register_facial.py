# backend/routers/register_facial.py

from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from models.autenticacion_facial import AutenticacionFacial
from models.codigo_qr import CodigoQR
from utils.security import hash_password
from utils.image_tools import redimensionar_imagen_base64
from utils.pdf_tools import generar_credencial_pdf
from utils.email_smtp import enviar_credencial_pdf
from datetime import datetime
import base64, requests, qrcode, io, os, hashlib

router = APIRouter(prefix="/register-facial", tags=["Registro Facial"])

SERVER_URL = "http://www.server.daossystem.pro:3405/Rostro"


# ──────────────────────────────────────────────
# Función auxiliar: segmentar rostro con DaosSystem
# ──────────────────────────────────────────────
def segmentar_rostro(img_b64: str) -> str:
    """Llama al servicio externo para segmentar y devuelve el rostro en base64."""
    try:
        resp = requests.post(
            f"{SERVER_URL}/Segmentar",
            json={"RostroA": img_b64},
            timeout=10
        )
    except Exception as e:
        raise HTTPException(502, f"No se pudo contactar al servidor de segmentación: {e}")

    if resp.status_code != 200:
        raise HTTPException(502, "Error al segmentar rostro (servidor externo).")

    data = resp.json()
    rostro_segmentado = data.get("rostro") or data.get("Rostro")
    if not rostro_segmentado:
        raise HTTPException(422, "El servicio no devolvió un rostro segmentado.")
    return rostro_segmentado


# ──────────────────────────────────────────────
# Endpoint principal: registro facial completo
# ──────────────────────────────────────────────
@router.post("/")
async def register_facial_user(
    usuario: str = Form(...),
    email: str = Form(...),
    nombre_completo: str = Form(...),
    password: str = Form(...),
    telefono: str = Form(...),
    rostro: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1️⃣ Validaciones básicas
    if db.query(Usuario).filter(Usuario.usuario == usuario).first():
        raise HTTPException(400, "⚠️ El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(400, "⚠️ El correo ya está registrado")
    if not rostro.content_type or "image" not in rostro.content_type:
        raise HTTPException(400, "El archivo subido debe ser una imagen válida")

    # 2️⃣ Convertir imagen a base64
    raw = await rostro.read()
    img_b64 = base64.b64encode(raw).decode("utf-8")
    try:
        img_b64 = redimensionar_imagen_base64(img_b64)
    except Exception:
        pass

    # 3️⃣ Segmentar rostro con DaosSystem
    rostro_segmentado_b64 = segmentar_rostro(img_b64)

    # 4️⃣ Crear usuario
    nuevo_usuario = Usuario(
        usuario=usuario.strip(),
        email=email.strip(),
        nombre_completo=nombre_completo.strip(),
        password_hash=hash_password(password),
        telefono=telefono.strip(),
        activo=True,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 5️⃣ Guardar autenticación facial
    facial = AutenticacionFacial(
        usuario_id=nuevo_usuario.id,
        encoding_facial="SEGMENTADO",
        imagen_referencia=rostro_segmentado_b64,
        activo=True,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(facial)
    db.commit()

    # 6️⃣ Generar QR de acceso (PNG + hash + URL)
    qr_text = f"https://simpaut.com/acceso/{nuevo_usuario.id}"

    # Generar imagen QR
    qr_img = qrcode.make(qr_text)
    qr_bytes = io.BytesIO()
    qr_img.save(qr_bytes, format="PNG")

    # Guardar la imagen localmente
    qr_dir = "pruebas/qr"
    os.makedirs(qr_dir, exist_ok=True)
    qr_filename = f"qr_{nuevo_usuario.id}.png"
    qr_path = os.path.join(qr_dir, qr_filename)
    with open(qr_path, "wb") as f:
        f.write(qr_bytes.getvalue())

    # Generar hash único del enlace QR
    qr_hash = hashlib.sha256(qr_text.encode()).hexdigest()

    # Registrar en base de datos (sin base64)
    codigo_qr = CodigoQR(
        usuario_id=nuevo_usuario.id,
        codigo_qr=qr_text,   # URL corta (menor a 555 chars)
        qr_hash=qr_hash,
        activo=True
    )
    db.add(codigo_qr)
    db.commit()

    # 7️⃣ Generar credencial PDF (usando la imagen del rostro y QR)
    output_dir = "pruebas/credenciales"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"credencial_{nuevo_usuario.id}.pdf")

    # Convertir imagen QR a base64 (para incrustar en PDF)
    qr_base64 = base64.b64encode(open(qr_path, "rb").read()).decode("utf-8")

    generar_credencial_pdf(
        nombre=nuevo_usuario.nombre_completo,
        correo=nuevo_usuario.email,
        usuario=nuevo_usuario.usuario,
        telefono=nuevo_usuario.telefono,
        qr_base64=qr_base64,
        rostro_base64=rostro_segmentado_b64,
        output_path=pdf_path
    )

    # 8️⃣ Enviar credencial por correo
    enviar_credencial_pdf(
        destinatario=nuevo_usuario.email,
        nombre_usuario=nuevo_usuario.nombre_completo,
        pdf_path=pdf_path
    )

    # ✅ Respuesta final
    return {
        "ok": True,
        "mensaje": "✅ Usuario registrado con rostro, QR y credencial enviada al correo",
        "usuario_id": nuevo_usuario.id,
        "email": nuevo_usuario.email,
        "qr_url": qr_text,
        "qr_hash": qr_hash
    }