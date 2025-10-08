# routers/register_facial.py
from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db             # usa tu get_db real aquí
from models.usuario import Usuario
from models.autenticacion_facial import AutenticacionFacial
from utils.security import hash_password
from utils.image_tools import redimensionar_imagen_base64  # si no lo quieres, elimínalo
from datetime import datetime
import base64, requests

router = APIRouter(prefix="/register-facial", tags=["Registro Facial"])

SERVER_URL = "http://www.server.daossystem.pro:3405/Rostro"

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
    rostro_segmentado = data.get("rostro") or data.get("Rostro")  # por si cambian la key
    if not rostro_segmentado:
        raise HTTPException(422, "El servicio no devolvió un rostro segmentado.")

    return rostro_segmentado

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
    # 1) Validaciones básicas
    if db.query(Usuario).filter(Usuario.usuario == usuario).first():
        raise HTTPException(400, "⚠️ El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(400, "⚠️ El correo ya está registrado")
    if not rostro.content_type or "image" not in rostro.content_type:
        raise HTTPException(400, "El archivo subido debe ser una imagen")

    # 2) Convertir imagen a base64 (y opcionalmente redimensionar para acelerar)
    raw = await rostro.read()
    img_b64 = base64.b64encode(raw).decode("utf-8")
    try:
        img_b64 = redimensionar_imagen_base64(img_b64)  # si no quieres, comenta esta línea
    except Exception:
        # no es crítico si falla el resize
        pass

    # 3) Segmentar con DaosSystem
    rostro_segmentado_b64 = segmentar_rostro(img_b64)

    # 4) Crear usuario
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

    # 5) Guardar biometría (usamos la imagen segmentada como referencia)
    facial = AutenticacionFacial(
        usuario_id=nuevo_usuario.id,
        encoding_facial="SEGMENTADO",         # placeholder si no usas embeddings
        imagen_referencia=rostro_segmentado_b64,
        activo=True,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(facial)
    db.commit()

    return {
        "ok": True,
        "mensaje": "✅ Usuario registrado con rostro segmentado",
        "usuario_id": nuevo_usuario.id,
    }