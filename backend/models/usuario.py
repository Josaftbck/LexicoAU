from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    # Relaciones
    facial = relationship("AutenticacionFacial", back_populates="usuario", uselist=False)
    qr = relationship("CodigoQR", back_populates="usuario", uselist=False)
    sesiones = relationship("Sesion", back_populates="usuario")