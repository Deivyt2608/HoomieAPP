from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session
from models.user import User
from database.connection import SessionLocal
from fastapi import HTTPException
from utils.email import enviar_correo_bienvenida
import asyncio
from fastapi.responses import RedirectResponse

router = APIRouter() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro")
async def registrar_usuario(
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    phone_usuario: str = Form(...),
    email_usuario: str = Form(...),
    contraseña_usuario: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar si el correo ya existe
    usuario_existente = db.query(User).filter(User.email == email_usuario).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    nuevo_usuario = User(
        nombre=nombre_usuario,
        apellido=apellido_usuario,
        phone=phone_usuario,
        email=email_usuario,
        password=contraseña_usuario
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Enviar correo de bienvenida (de forma asíncrona)
    asyncio.create_task(enviar_correo_bienvenida(email_usuario, nombre_usuario))

    #✅ Iniciar sesión automáticamente al guardar
    resp = RedirectResponse(url="/inicio", status_code=302)
    resp.set_cookie(key="usuario_email", value=nuevo_usuario.email)
    return resp

