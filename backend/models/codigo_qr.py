# backend/models/codigo_qr.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CodigoQR(Base):
    __tablename__ = "codigos_qr"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    codigo_qr = Column(String(555), nullable=False, unique=True)
    qr_hash = Column(String(555), nullable=False)
    activo = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="qr")