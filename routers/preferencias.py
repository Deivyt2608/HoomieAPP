# routers/preferencias.py
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
from models.preferencias import Preference

router = APIRouter()

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
