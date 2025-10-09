# backend/routers/login_qr.py
from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from models.codigo_qr import CodigoQR
from models.sesion import Sesion, MetodoLoginEnum
from utils.security import crear_token_jwt
from datetime import datetime
import hashlib
import secrets

router = APIRouter(prefix="/login-qr", tags=["Login QR"])

@router.post("/")
def login_qr(qr_hash: str = Form(...), db: Session = Depends(get_db)):
    """
    Autentica a un usuario escaneando su QR (basado en qr_hash).
    """
    # 1️⃣ Buscar QR en la base de datos
    qr_entry = db.query(CodigoQR).filter(
        CodigoQR.qr_hash == qr_hash,
        CodigoQR.activo == True
    ).first()

    if not qr_entry:
        raise HTTPException(401, detail="❌ Código QR inválido o inactivo")

    # 2️⃣ Obtener usuario asociado
    usuario = db.query(Usuario).filter(Usuario.id == qr_entry.usuario_id).first()
    if not usuario or not usuario.activo:
        raise HTTPException(403, detail="⚠️ Usuario inactivo o inexistente")

    # 3️⃣ Generar token de sesión (JWT o aleatorio)
    session_token = secrets.token_hex(32)

    # 4️⃣ Registrar sesión en BD
    nueva_sesion = Sesion(
        usuario_id=usuario.id,
        session_token=session_token,
        metodo_login=MetodoLoginEnum.qr,
        activa=True,
        fecha_login=datetime.utcnow()
    )
    db.add(nueva_sesion)
    db.commit()

    # 5️⃣ Retornar datos del usuario + token
    return {
        "ok": True,
        "mensaje": "✅ Sesión iniciada correctamente mediante QR",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre_completo,
            "email": usuario.email,
            "telefono": usuario.telefono,
        },
        "token_sesion": session_token
    }