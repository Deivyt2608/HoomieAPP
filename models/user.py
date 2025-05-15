from sqlalchemy import Column, Integer, String
from database.connection import Base
from sqlalchemy.orm import relationship
from models.preferencias import Preference


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    foto = Column(String(200), nullable=True)
    publicaciones = relationship("Publicacion", back_populates="usuario")
    preferences = relationship("Preference", back_populates="usuario", uselist=False)


