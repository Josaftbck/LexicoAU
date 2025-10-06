from fastapi import APIRouter, HTTPException, Depends, Form, Header, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal
from models.usuario import Usuario
from models.autenticacion_facial import AutenticacionFacial
from schemas.usuario import UsuarioCreate, UsuarioLogin
from utils.security import hash_password, verify_password
from utils.jwt_manager import create_access_token, verify_access_token
from utils.luxand_api import verify_face, register_face
from utils.image_tools import redimensionar_imagen_base64
import base64
from datetime import datetime

router = APIRouter()

# ==== Dependencia para obtener la sesión de DB ====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==== Registro de nuevo usuario (sin rostro) ====
@router.post("/register")
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.usuario == usuario.usuario).first():
        raise HTTPException(status_code=400, detail="⚠️ El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="⚠️ El correo ya está registrado")

    try:
        hashed_password = hash_password(usuario.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    nuevo_usuario = Usuario(
        usuario=usuario.usuario,
        email=usuario.email,
        nombre_completo=usuario.nombre_completo,
        password_hash=hashed_password,
        telefono=usuario.telefono,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "✅ Usuario creado correctamente",
        "usuario_id": nuevo_usuario.id
    }

# ==== Login con JWT ====
@router.post("/login")
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.usuario == data.usuario).first()
    if not user:
        raise HTTPException(status_code=401, detail="❌ Usuario no encontrado")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="❌ Contraseña incorrecta")
    if not user.activo:
        raise HTTPException(status_code=403, detail="⛔ Usuario inactivo")

    token_data = {"sub": user.usuario}
    access_token = create_access_token(token_data)

    return {
        "mensaje": "✅ Login exitoso",
        "access_token": access_token,
        "token_type": "bearer",
        "usuario_id": user.id
    }

# ==== Ruta protegida ====
def get_current_user(authorization: str = Header(...)):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="⚠️ Formato del token inválido")

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="⚠️ Token inválido o expirado")

    return payload

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "mensaje": f"🔒 Acceso concedido a: {current_user['sub']}"
    }

# ==== Verificar rostro (Luxand compara la foto actual vs. la de la base) ====
@router.post("/verify-face")
def verificar_rostro(
    file: UploadFile = File(...),
    usuario_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar usuario
    empleado = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="❌ Usuario no encontrado")

    # Obtener datos faciales del usuario
    facial_data = db.query(AutenticacionFacial).filter(AutenticacionFacial.usuario_id == usuario_id).first()
    if not facial_data or not facial_data.imagen_referencia:
        raise HTTPException(status_code=404, detail="❌ No se encontró imagen de referencia")

    # Convertir imagen enviada a base64
    uploaded_image_bytes = file.file.read()
    uploaded_image_b64 = base64.b64encode(uploaded_image_bytes).decode("utf-8")

    # Enviar a Luxand
    resultado = verify_face(uploaded_image_b64, facial_data.imagen_referencia)

    if not resultado["success"]:
        raise HTTPException(status_code=400, detail="❌ Error en Luxand: " + resultado["error"])

    return {
        "mensaje": "✅ Comparación completada",
        "score": f"{resultado['score'] * 100:.2f}%",
        "similar": resultado["similar"]
    }
# ==== Registro de usuario con foto y rostro ====
@router.post("/register-with-photo")
async def register_with_photo(
    usuario: str = Form(...),
    email: str = Form(...),
    nombre_completo: str = Form(...),
    password: str = Form(...),
    telefono: str = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).filter(Usuario.usuario == usuario).first():
        raise HTTPException(status_code=400, detail="⚠️ El usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="⚠️ El correo ya está registrado")

    try:
        hashed_password = hash_password(password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    foto_bytes = await foto.read()
    foto_b64 = base64.b64encode(foto_bytes).decode("utf-8")
    foto_b64 = redimensionar_imagen_base64(foto_b64)

    luxand_response = register_face(usuario, foto_b64)

    if not luxand_response.get("success"):
        raise HTTPException(status_code=500, detail=f"❌ Error al registrar rostro: {luxand_response.get('error')}")

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

    nueva_autenticacion = AutenticacionFacial(
        usuario_id=nuevo_usuario.id,
        encoding_facial=luxand_response.get("embedding") or "PENDING",
        imagen_referencia=foto_b64,
        activo=True,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nueva_autenticacion)
    db.commit()

    return {
        "mensaje": "✅ Usuario registrado con reconocimiento facial",
        "usuario_id": nuevo_usuario.id
    }