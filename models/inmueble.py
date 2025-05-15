from sqlalchemy import Column, Integer, String, Boolean, Text
from database.connection import Base
from sqlalchemy.orm import relationship

class Inmueble(Base):
    __tablename__ = "inmuebles"

    id = Column(Integer, primary_key=True, index=True)

    tipo_inmueble = Column(String(50), nullable=False)  # apartamento, casa
    direccion = Column(String(200), nullable=False)
    barrio = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)

    valor_arriendo = Column(Integer, nullable=False)
    valor_administracion = Column(Integer, nullable=True)
    area_m2 = Column(Integer, nullable=False)
    num_habitaciones = Column(Integer, nullable=False)
    num_banos = Column(Integer, nullable=False)
    num_parqueaderos = Column(Integer, nullable=False)
    estrato = Column(Integer, nullable=False)

    genero_preferido = Column(String(20), nullable=False)  # masculino, femenino, indiferente
    permite_mascotas = Column(Boolean, default=False)
    permite_fumadores = Column(Boolean, default=False)
    permite_fiestas = Column(Boolean, default=False)

    fotos = Column(Text, nullable=True)  # rutas separadas por comas

    publicacion = relationship("Publicacion", back_populates="inmueble", uselist=False)
