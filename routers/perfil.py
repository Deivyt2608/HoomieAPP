# routers/perfil.py
from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
import shutil, os

router = APIRouter()
UPLOAD_DIR = "static/imagenes/usuarios"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/editar-perfil")
async def actualizar_perfil(
    request: Request,
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    phone_usuario: str = Form(...),
    email_usuario: str = Form(...),
    foto_usuario: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        return RedirectResponse("/perfil?mensaje=usuario_no_encontrado", status_code=302)

    usuario.nombre = nombre_usuario
    usuario.apellido = apellido_usuario
    usuario.phone = phone_usuario

    if foto_usuario:
        ext = os.path.splitext(foto_usuario.filename)[1]
        filename = f"{usuario.id}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto_usuario.file, buffer)
        usuario.foto = f"/static/imagenes/usuarios/{filename}"

    db.commit()
    return RedirectResponse("/perfil?mensaje=perfil_actualizado", status_code=302)
