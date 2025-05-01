from sqlalchemy import Column, Integer, String, Text
from database.connection import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Apartamento(Base):
    __tablename__ = "apartamentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    usuario = relationship("User", back_populates="apartamentos")
    precio = Column(Integer, nullable=False)
    tipo = Column(String(100), nullable=False)
    area = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=False)
    direccion = Column(String(200), nullable=False)
    barrio = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False) 
    contacto = Column(String(100), nullable=False)
    imagenes = Column(Text, nullable=True) 
