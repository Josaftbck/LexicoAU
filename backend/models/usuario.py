
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from database import Base
from datetime import datetime  # ✅ Import necesario

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)  # ✅ Corregido
    activo = Column(Boolean, default=True)