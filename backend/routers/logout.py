from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from utils.security import verificar_token_jwt
from models.sesion import Sesion

router = APIRouter(prefix="/logout", tags=["Autenticación"])

@router.post("/")
def cerrar_sesion(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Cierra la sesión activa del usuario basada en su token JWT.
    Marca la sesión como inactiva en la tabla 'sesiones'.
    """
    # 1️⃣ Verificar que venga el encabezado correcto
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="❌ Token no válido o faltante")

    token = authorization.split(" ")[1]

    # 2️⃣ Verificar la validez del token
    try:
        payload = verificar_token_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

    usuario_id = payload.get("sub")
    if not usuario_id:
        raise HTTPException(status_code=400, detail="❌ Token sin ID de usuario")

    # 3️⃣ Buscar la sesión activa con ese token
    sesion = (
        db.query(Sesion)
        .filter(
            Sesion.usuario_id == usuario_id,
            Sesion.session_token == token,
            Sesion.activa == True
        )
        .first()
    )

    if not sesion:
        raise HTTPException(status_code=404, detail="⚠️ Sesión no encontrada o ya cerrada")

    # 4️⃣ Cerrar la sesión
    sesion.activa = False
    db.commit()

    return {
        "ok": True,
        "mensaje": "✅ Sesión cerrada correctamente",
        "usuario_id": usuario_id
    }