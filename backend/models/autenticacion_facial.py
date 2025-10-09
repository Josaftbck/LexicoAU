from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AutenticacionFacial(Base):
    __tablename__ = "autenticacion_facial"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    encoding_facial = Column(Text, nullable=False)
    imagen_referencia = Column(Text)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación inversa con Usuario
    usuario = relationship("Usuario", back_populates="facial")