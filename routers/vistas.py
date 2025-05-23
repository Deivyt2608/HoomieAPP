from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.session import get_usuario_logueado
from sqlalchemy.orm import Session
from database.connection import get_db
from models.publicacion import Publicacion

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Ruta relativa desde main.py

@router.get("/base", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("base.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
    })

@router.get("/inicio", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("inicio.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
    })

@router.get("/perfil", response_class=HTMLResponse)
async def ver_perfil(request: Request, db: Session = Depends(get_db)):
    usuario = get_usuario_logueado(request)
    if not usuario:
        return templates.TemplateResponse("perfil.html", {
            "request": request,
            "usuario_logueado": None,
            "publicaciones": []
        })

    publicaciones = db.query(Publicacion).filter(Publicacion.usuario_id == usuario.id).all()

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario_logueado": usuario,
        "publicaciones": publicaciones
    })


@router.get("/publicar", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("publica_apto.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
    })

@router.get("/trabajo", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("trabajo.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
    })

@router.get("/match", response_class=HTMLResponse)
async def inicio(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("match.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
    })

@router.get("/apto", response_class=HTMLResponse)
async def mostrar_formulario_inmueble(request: Request, publicacion_id: int):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("apto.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None,
        "publicacion_id": publicacion_id
    })

@router.get("/nosotros", response_class=HTMLResponse)
async def mostrar_formulario_inmueble(request: Request):
    usuario = get_usuario_logueado(request)
    return templates.TemplateResponse("conocenos.html", {
        "request": request,
        "usuario_logueado": usuario if usuario else None
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
    ("/nosotros", "conocenos.html"),
    ("/olvida", "olvida.html"),
    ("/perfil", "perfil.html"),
    ("/registro", "registro.html"),
    ("/rentar", "rentar.html"),
    ("/trabajo", "trabajo.html"),
    ("/restablecer","restablecer.html"),
    ("/publica_apto","publica_apto.html"),
    ("/apto","apto.html"),
    ("/formulario-match", "match.html")
]

# Registro dinámico de rutas
for path, template in routes:
    router.add_api_route(path, render_template(template), methods=["GET"], response_class=HTMLResponse)



