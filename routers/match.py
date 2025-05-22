from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.connection import get_db
from utils.session import get_usuario_logueado
from models.user import User
from models.preferencias import Preference
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def bin_to_num(valor: str) -> int:
    return 5 if valor.lower() == "sí" else 0


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/match/{usuario_id}", response_class=HTMLResponse)
def ver_match(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    usuario_actual = get_usuario_logueado(request)
    if not usuario_actual:
        return RedirectResponse("/ingreso?mensaje=sesion_requerida", status_code=302)

    preferencias_1 = db.query(Preference).filter(Preference.user_id == usuario_actual.id).first()
    preferencias_2 = db.query(Preference).filter(Preference.user_id == usuario_id).first()
    usuario_2 = db.query(User).filter(User.id == usuario_id).first()

    if not preferencias_1 or not preferencias_2:
        return templates.TemplateResponse("match.html", {
            "request": request,
            "compatibilidad": None,
            "usuario_logueado": usuario_actual,
            "usuario_objetivo": usuario_2,
            "incompleto": True
        })

    vector_1 = np.array([[preferencias_1.aseo_hogar, preferencias_1.ruido_hogar, preferencias_1.visitas,
                          preferencias_1.aseo_personal, preferencias_1.division_tareas, preferencias_1.salidas_fiesta]])
    vector_2 = np.array([[preferencias_2.aseo_hogar, preferencias_2.ruido_hogar, preferencias_2.visitas,
                          preferencias_2.aseo_personal, preferencias_2.division_tareas, preferencias_2.salidas_fiesta]])

    resultado = cosine_similarity(vector_1, vector_2)[0][0] * 100

    return templates.TemplateResponse("match.html", {
        "request": request,
        "compatibilidad": round(resultado, 2),
        "usuario_logueado": usuario_actual,
        "usuario_objetivo": usuario_2,
        "incompleto": False
    })

@router.get("/match/api/{usuario_id}")
def obtener_compatibilidad(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    usuario_actual = get_usuario_logueado(request)
    if not usuario_actual:
        return JSONResponse(status_code=401, content={"error": "No autenticado"})

    preferencias_1 = db.query(Preference).filter(Preference.user_id == usuario_actual.id).first()
    preferencias_2 = db.query(Preference).filter(Preference.user_id == usuario_id).first()

    if not preferencias_1 or not preferencias_2:
        return JSONResponse(content={"incompleto": True})

    vector_1 = [[
    preferencias_1.aseo_hogar,
    preferencias_1.ruido_hogar,
    preferencias_1.visitas,
    preferencias_1.aseo_personal,
    preferencias_1.division_tareas,
    preferencias_1.salidas_fiesta,
    bin_to_num(preferencias_1.fuma),
    bin_to_num(preferencias_1.alcohol),
    bin_to_num(preferencias_1.trabaja_casa),
    bin_to_num(preferencias_1.mascotas),
    bin_to_num(preferencias_1.estudia),
    bin_to_num(preferencias_1.trabaja)
    ]]

    vector_2 = [[
        preferencias_2.aseo_hogar,
        preferencias_2.ruido_hogar,
        preferencias_2.visitas,
        preferencias_2.aseo_personal,
        preferencias_2.division_tareas,
        preferencias_2.salidas_fiesta,
        bin_to_num(preferencias_2.fuma),
        bin_to_num(preferencias_2.alcohol),
        bin_to_num(preferencias_2.trabaja_casa),
        bin_to_num(preferencias_2.mascotas),
        bin_to_num(preferencias_2.estudia),
        bin_to_num(preferencias_2.trabaja)
    ]]

    resultado = cosine_similarity(vector_1, vector_2)[0][0] * 100

    return JSONResponse(content={
        "compatibilidad": round(resultado, 2),
        "usuario_id": usuario_id
    })
