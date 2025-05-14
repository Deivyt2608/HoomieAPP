# models/preferences.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    aseo_hogar = Column(Integer)
    ruido_hogar = Column(Integer)
    visitas = Column(Integer)
    aseo_personal = Column(Integer)
    division_tareas = Column(Integer)
    salidas_fiesta = Column(Integer)

    fuma = Column(String(10))
    alcohol = Column(String(10))
    trabaja_casa = Column(String(10))
    mascotas = Column(String(10))
    estudia = Column(String(10))
    trabaja = Column(String(10))

    usuario = relationship("User", back_populates="preferences")
