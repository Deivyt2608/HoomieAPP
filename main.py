from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import publicacion, vistas, auth, usuario, perfil, preferencias, publicaciones, detalle
from database.connection import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Incluir routers
app.include_router(vistas.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(perfil.router)
app.include_router(publicacion.router)
app.include_router(preferencias.router)
app.include_router(publicaciones.router)
app.include_router(detalle.router)
