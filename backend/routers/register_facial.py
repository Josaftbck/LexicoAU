from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario import Usuario
from models.autenticacion_facial import AutenticacionFacial
from utils.security import hash_password
from utils.image_tools import redimensionar_imagen_base64
from datetime import datetime
import base64

router = APIRouter(prefix="/register-facial", tags=["Registro Facial"])

# ==== Dependencia para obtener DB ====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==== Registro facial (sin Luxand) ====
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
    # 🧩 Validar duplicados
    if db.query(Usuario).filter(Usuario.usuario == usuario).first():
        raise HTTPException(status_code=400, detail="⚠️ El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="⚠️ El correo ya está registrado")

    # 🔐 Hashear contraseña
    hashed_password = hash_password(password)

    # 📸 Convertir imagen a Base64
    rostro_bytes = await rostro.read()
    rostro_b64 = base64.b64encode(rostro_bytes).decode("utf-8")

    # 🧩 Redimensionar (opcional)
    rostro_b64 = redimensionar_imagen_base64(rostro_b64)

    # 💾 Crear usuario
    nuevo_usuario = Usuario(
        usuario=usuario.strip(),
        email=email.strip(),
        nombre_completo=nombre_completo.strip(),
        password_hash=hashed_password,
        telefono=telefono.strip(),
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # 💾 Guardar datos biométricos (segmentados)
    nueva_autenticacion = AutenticacionFacial(
        usuario_id=nuevo_usuario.id,
        encoding_facial="NO_EMBEDDING",  # Placeholder si no se usa Luxand
        imagen_referencia=rostro_b64,
        activo=True,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nueva_autenticacion)
    db.commit()

    return {
        "mensaje": "✅ Usuario registrado correctamente con segmentación de datos",
        "usuario_id": nuevo_usuario.id
    }
