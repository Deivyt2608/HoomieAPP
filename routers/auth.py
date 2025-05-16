from fastapi import APIRouter, Form, Response, Request, Depends,HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
from fastapi import Form
from utils.email import enviar_enlace_restablecer

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(
    response: Response,
    email_usuario: str = Form(...),
    pass_usuario: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario or usuario.password != pass_usuario:
        return RedirectResponse(url=f"/ingreso?mensaje=error&correo={email_usuario}", status_code=302)

    # Guardar cookie para saber que está logueado
    resp = RedirectResponse(url="/inicio?mensaje=exito", status_code=302)
    resp.set_cookie(key="usuario_email", value=usuario.email)
    return resp

@router.get("/logout")
def logout(response: Response):
    resp = RedirectResponse(url="/inicio", status_code=302)
    resp.delete_cookie("usuario_email")
    return resp

@router.post("/enviar-enlace")
async def enviar_enlace(email_usuario: str = Form(...), db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        # Redirige con mensaje y reenvía el correo para que se mantenga el campo
        return RedirectResponse(url=f"/olvida?mensaje=correo_no_encontrado&correo={email_usuario}", status_code=302)

    token = usuario.email  # en producción deberías usar un token único y temporal
    enlace = f"https://hoomieapp.onrender.com/restablecer?token={token}"

    await enviar_enlace_restablecer(usuario.email, usuario.nombre, enlace)
    return RedirectResponse(url="/ingreso?mensaje=verifica_tu_correo", status_code=302)

@router.post("/guardar-nueva")
async def guardar_nueva(
    email_usuario: str = Form(...),
    nueva_contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(User).filter(User.email == email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Correo no encontrado")

    usuario.password = nueva_contraseña
    db.commit()
    return RedirectResponse(url="/ingreso?mensaje=contraseña_actualizada", status_code=302)
