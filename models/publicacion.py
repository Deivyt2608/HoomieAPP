from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Publicacion(Base):
    __tablename__ = "publicaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    tipo_publicacion = Column(String(30), nullable=False)  # 'arrendar' o 'buscar roomie'
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    inmueble_id = Column(Integer, ForeignKey("inmuebles.id"), nullable=True)

    usuario = relationship("User", back_populates="publicaciones")
    inmueble = relationship("Inmueble", back_populates="publicacion")
