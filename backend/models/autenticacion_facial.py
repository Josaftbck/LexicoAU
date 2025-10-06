from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from database import Base
from datetime import datetime

class AutenticacionFacial(Base):
    __tablename__ = "autenticacion_facial"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    encoding_facial = Column(Text)  # embedding o vector Luxand
    imagen_referencia = Column(Text)  # foto en base64
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)