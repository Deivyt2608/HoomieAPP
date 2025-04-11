from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import vistas, auth, usuario, perfil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Incluir routers
app.include_router(vistas.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(perfil.router)