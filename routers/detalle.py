# routers/publicaciones.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.publicacion import Publicacion
from models.user import User
from utils.session import get_usuario_logueado
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/detalle/{publicacion_id}", response_class=HTMLResponse)
async def ver_detalle_publicacion(publicacion_id: int, request: Request, db: Session = Depends(get_db)):
    publicacion = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()
    if not publicacion:
        return RedirectResponse("/publicaciones?mensaje=no_encontrada", status_code=302)

    usuario = get_usuario_logueado(request)

    return templates.TemplateResponse("detalle.html", {
        "request": request,
        "publicacion": publicacion,
        "usuario_logueado": usuario
    })
