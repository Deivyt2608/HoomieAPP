# reset_db.py
from database.connection import Base, engine
from models.inmueble import Inmueble
from models.user import User
from models.publicacion import Publicacion
from models.preferencias import Preference


# Elimina todas las tablas
print("🔴 Eliminando todas las tablas...")
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)