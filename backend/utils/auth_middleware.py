# backend/utils/auth_middleware.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from database import get_db
from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.sesion import Sesion
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_super_secreta")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

async def verificar_sesion_activa(request: Request, db: Session = None):
    """Verifica que el token sea válido y que la sesión esté activa en BD."""
    authorization: str = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # Abrir DB si no viene del endpoint
    if db is None:
        from database import SessionLocal
        db = SessionLocal()

    sesion = db.query(Sesion).filter(
        Sesion.usuario_id == usuario_id,
        Sesion.session_token == token,
        Sesion.activa == True
    ).first()

    if not sesion:
        raise HTTPException(status_code=401, detail="Sesión no válida o cerrada")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.activo == True).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario inactivo o no encontrado")

    return usuario