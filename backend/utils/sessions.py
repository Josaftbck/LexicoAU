from sqlalchemy.orm import Session
from models.sesion import Sesion, MetodoLogin
from datetime import datetime

def registrar_sesion(db: Session, usuario_id: int, token: str, metodo: str):
    """
    Registra una nueva sesión JWT activa en la base de datos.
    """
    sesion = Sesion(
        usuario_id=usuario_id,
        session_token=token,
        metodo_login=MetodoLogin(metodo),
        fecha_login=datetime.utcnow(),
        activa=True
    )
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion