# routers/preferencias.py
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
from models.preferencias import Preference
from utils.session import get_usuario_logueado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guardar-preferencias")
async def guardar_preferencias(
    request: Request,
    aseo_hogar: int = Form(...),
    ruido_hogar: int = Form(...),
    visitas: int = Form(...),
    aseo_personal: int = Form(...),
    division_tareas: int = Form(...),
    salidas_fiesta: int = Form(...),
    fuma: str = Form(...),
    alcohol: str = Form(...),
    trabaja_casa: str = Form(...),
    mascotas: str = Form(...),
    estudia: str = Form(...),
    trabaja: str = Form(...),
    db: Session = Depends(get_db)
):
    email_usuario = request.cookies.get("usuario_email")
    if not email_usuario:
        return RedirectResponse(url="/ingreso?mensaje=sesion_requerida", status_code=302)

    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        return RedirectResponse(url="/ingreso?mensaje=sesion_requerida", status_code=302)

    preferencias = db.query(Preference).filter(Preference.user_id == usuario.id).first()

    if not preferencias:
        preferencias = Preference(user_id=usuario.id)
        db.add(preferencias)

    preferencias.aseo_hogar = aseo_hogar
    preferencias.ruido_hogar = ruido_hogar
    preferencias.visitas = visitas
    preferencias.aseo_personal = aseo_personal
    preferencias.division_tareas = division_tareas
    preferencias.salidas_fiesta = salidas_fiesta
    preferencias.fuma = fuma
    preferencias.alcohol = alcohol
    preferencias.trabaja_casa = trabaja_casa
    preferencias.mascotas = mascotas
    preferencias.estudia = estudia
    preferencias.trabaja = trabaja

    db.commit()
    return RedirectResponse(url="/inicio?mensaje=preferencias_guardadas", status_code=302)


@router.get("/editar-preferencias", response_class=HTMLResponse)
def editar_preferencias(request: Request, db: Session = Depends(get_db), usuario=Depends(get_usuario_logueado)):
    preferencias = db.query(Preference).filter(Preference.usuario == usuario).first()
    preferencias_dict = {
    "aseo_hogar": preferencias.aseo_hogar,
    "ruido_hogar": preferencias.ruido_hogar,
    "visitas": preferencias.visitas,
    "aseo_personal": preferencias.aseo_personal,
    "division_tareas": preferencias.division_tareas,
    "salidas_fiesta": preferencias.salidas_fiesta,
    "fuma": preferencias.fuma,
    "alcohol": preferencias.alcohol,
    "trabaja_casa": preferencias.trabaja_casa,
    "mascotas": preferencias.mascotas,
    "estudia": preferencias.estudia,
    "trabaja": preferencias.trabaja
    } if preferencias else None

    return templates.TemplateResponse("match.html", {
    "request": request,
    "preferencias_guardadas": preferencias_dict
})