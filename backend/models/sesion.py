from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

# Usamos un Enum de Python para validar en código,
# pero en DB guardamos texto para evitar problemas de tipo.
class MetodoLoginEnum(str, enum.Enum):
    password = "password"
    facial   = "facial"
    qr       = "qr"

class Sesion(Base):
    __tablename__ = "sesiones"

    id            = Column(Integer, primary_key=True, index=True)
    usuario_id    = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    session_token = Column(String(255), nullable=False)

    # Guarda como texto; así evitas conflictos de Enum con MySQL
    metodo_login  = Column(String(12), nullable=False, default=MetodoLoginEnum.qr.value)

    fecha_login   = Column(TIMESTAMP, default=datetime.utcnow)
    activa        = Column(Boolean, default=True)

    usuario       = relationship("Usuario", back_populates="sesiones")