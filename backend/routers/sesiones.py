# backend/routers/sesiones.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from utils.auth_middleware import verificar_sesion_activa
from models.sesion import Sesion

router = APIRouter(prefix="/sesiones", tags=["Sesiones"])

@router.get("/activas")
async def listar_sesiones_activas(request: Request, db: Session = Depends(get_db)):
    """Devuelve todas las sesiones activas del usuario logueado."""
    usuario = await verificar_sesion_activa(request, db)
    sesiones = db.query(Sesion).filter(Sesion.usuario_id == usuario.id, Sesion.activa == True).all()

    return {
        "usuario": usuario.usuario,
        "total_activas": len(sesiones),
        "sesiones": [
            {
                "id": s.id,
                "metodo_login": s.metodo_login,
                "fecha_login": s.fecha_login.isoformat(),
                "activa": s.activa
            }
            for s in sesiones
        ]
    }