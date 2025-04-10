from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.session import get_usuario_logueado

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Ruta relativa desde main.py


@router.get("/inicio", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("inicio.html", {
        "request": request,
        "usuario_logueado": usuario.nombre if usuario else None
    })

@router.get("/perfil", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario_logueado": usuario.nombre if usuario else None
    })

# Función genérica para renderizar plantillas
def render_template(template_name: str):
    async def view(request: Request):
        return templates.TemplateResponse(template_name, {"request": request})
    return view

# Rutas disponibles
routes = [
    ("/", "inicio.html"),
    ("/inicio", "inicio.html"),
    ("/ingreso", "ingreso.html"),
    ("/conocenos", "conocenos.html"),
    ("/olvida", "olvida.html"),
    ("/perfil", "perfil.html"),
    ("/registro", "registro.html"),
    ("/rentar", "rentar.html"),
    ("/trabajo", "trabajo.html"),
    ("/restablecer","restablecer.html")
]

# Registro dinámico de rutas
for path, template in routes:
    router.add_api_route(path, render_template(template), methods=["GET"], response_class=HTMLResponse)



