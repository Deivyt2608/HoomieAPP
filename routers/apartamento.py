# routers/apartamento.py
from fastapi import APIRouter, Form, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.apartamento import Apartamento
from models.user import User
import shutil, os

router = APIRouter()

UPLOAD_DIR = "static/imagenes/apartamentos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/publicar-apartamento")
async def publicar_apartamento(
    request: Request,
    precio: int = Form(...),
    tipo: str = Form(...),
    area: int = Form(...),
    descripcion: str = Form(...),
    direccion: str = Form(...),
    barrio: str = Form(...),
    ciudad: str = Form(...),
    estado: str = Form(...),
    contacto: str = Form(...),
    fotos: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    # Verificar si hay sesión iniciada
    email_usuario = request.cookies.get("usuario_email")
    if not email_usuario:
        return RedirectResponse(url="/ingreso?mensaje=sesion_requerida", status_code=302)

    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    # Guardar las imágenes
    rutas_imagenes = []
    for foto in fotos:
        ext = os.path.splitext(foto.filename)[1]
        filename = f"{usuario.id}_{foto.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        rutas_imagenes.append(f"/static/imagenes/apartamentos/{filename}")

    # Crear el registro en la base de datos
    nuevo = Apartamento(
        usuario_id=usuario.id,
        precio=precio,
        tipo=tipo,
        area=area,
        descripcion=descripcion,
        direccion=direccion,
        barrio=barrio,
        ciudad=ciudad,
        estado=estado,
        contacto=contacto,
        imagenes=",".join(rutas_imagenes)
    )

    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/inicio?mensaje=publicacion_exitosa", status_code=302)
