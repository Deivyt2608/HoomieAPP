# routers/publicaciones.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.publicacion import Publicacion
from models.inmueble import Inmueble
from models.user import User
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/publicaciones", response_class=HTMLResponse)
async def ver_publicaciones(
    request: Request,
    tipo: str = "",
    ciudad: str = "",
    estrato: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Publicacion).join(Inmueble).filter(Publicacion.inmueble_id == Inmueble.id)

    if tipo:
        query = query.filter(Publicacion.tipo_publicacion == tipo)
    if ciudad:
        query = query.filter(Inmueble.ciudad.ilike(f"%{ciudad}%"))
    if estrato:
        query = query.filter(Inmueble.estrato == int(estrato))

    publicaciones = query.all()

    usuario_email = request.cookies.get("usuario_email")
    usuario = db.query(User).filter(User.email == usuario_email).first() if usuario_email else None

    return templates.TemplateResponse("publicaciones.html", {
        "request": request,
        "publicaciones": publicaciones,
        "usuario_logueado": usuario
    })
