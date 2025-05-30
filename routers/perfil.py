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
        return RedirectResponse("/ingreso?mensaje=usuario_no_encontrado", status_code=302)

    usuario.nombre = nombre_usuario
    usuario.apellido = apellido_usuario
    usuario.phone = phone_usuario

    if foto_usuario.content_type.startswith("image/"):
    # guardar archivo...

        if foto_usuario and foto_usuario.filename != "":
            import uuid
            filename = f"{uuid.uuid4().hex}_{foto_usuario.filename}"
            ruta_foto = os.path.join(UPLOAD_DIR, filename)

            with open(ruta_foto, "wb") as buffer:
                shutil.copyfileobj(foto_usuario.file, buffer)

            usuario.foto = "/" + ruta_foto.replace("\\", "/")  # ruta relativa

    db.commit()
    return RedirectResponse("/perfil?mensaje=perfil_actualizado", status_code=302)
