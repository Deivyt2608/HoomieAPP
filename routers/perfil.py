from fastapi import APIRouter, Form, UploadFile, File, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
import shutil
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from utils.session import get_usuario_desde_cookie

router = APIRouter()

UPLOAD_DIR = "static/imagenes/usuarios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/perfil/editar")
async def editar_perfil(
    request: Request,
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    phone_usuario: str = Form(...),
    email_usuario: str = Form(...),
    contraseña_usuario: str = Form(None),
    foto_usuario: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        return RedirectResponse(url="/perfil?error=usuario_no_encontrado", status_code=302)

    # Actualizar campos básicos
    usuario.nombre = nombre_usuario
    usuario.apellido = apellido_usuario
    usuario.phone = phone_usuario
    if contraseña_usuario:
        usuario.password = contraseña_usuario  # Aquí puedes aplicar hashing si lo activas luego

    # Procesar imagen si se envió
    if foto_usuario:
        extension = os.path.splitext(foto_usuario.filename)[1]
        filename = f"{usuario.id}{extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto_usuario.file, buffer)

        usuario.foto = f"/static/imagenes/usuarios/{filename}"

    db.commit()
    return RedirectResponse(url="/perfil?mensaje=perfil_actualizado", status_code=302)

templates = Jinja2Templates(directory="templates")

@router.get("/perfil", response_class=HTMLResponse)
async def mostrar_perfil(request: Request):
    usuario = get_usuario_desde_cookie(request)
    if not usuario:
        return RedirectResponse(url="/ingreso", status_code=302)

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario_logueado": usuario
    })