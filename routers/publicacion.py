# routers/publicacion.py
from fastapi import APIRouter, Form, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.publicacion import Publicacion
from models.inmueble import Inmueble
from models.user import User
import shutil, os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/crear-publicacion")
async def crear_publicacion(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo_publicacion: str = Form(...),
    db: Session = Depends(get_db)
):
    email = request.cookies.get("usuario_email")
    if not email:
        return RedirectResponse("/ingreso?mensaje=sesion_requerida", status_code=302)

    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        return RedirectResponse("/ingreso?mensaje=sesion_requerida", status_code=302)

    nueva_pub = Publicacion(
        nombre=nombre,
        descripcion=descripcion,
        tipo_publicacion=tipo_publicacion,
        usuario_id=usuario.id
    )
    db.add(nueva_pub)
    db.commit()
    db.refresh(nueva_pub)

    return RedirectResponse(f"/apto?publicacion_id={nueva_pub.id}", status_code=302)

UPLOAD_DIR = "static/imagenes/apartamentos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/publicar-inmueble")
async def publicar_apartamento(
    request: Request,

    publicacion_id: int = Form(...),
    tipo_inmueble: str = Form(...),
    direccion: str = Form(...),
    barrio: str = Form(...),
    ciudad: str = Form(...),

    valor_arriendo: int = Form(...),
    valor_administracion: int = Form(...),
    area_m2: int = Form(...),
    
    num_habitaciones: int = Form(...),
    num_banos: int = Form(...),
    num_parqueaderos: int = Form(...),
    estrato: int = Form(...),
    
    genero_preferido: str = Form(...),
    permite_mascotas: bool = Form(...),
    permite_fumadores: bool = Form(...),
    permite_fiestas: bool = Form(...),

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
    inmueble = Inmueble(
        tipo_inmueble=tipo_inmueble,
        direccion=direccion,
        barrio=barrio,
        ciudad=ciudad,

        valor_arriendo=valor_arriendo,
        valor_administracion=valor_administracion,
        area_m2=area_m2,
        num_habitaciones=num_habitaciones,
        num_banos=num_banos,
        num_parqueaderos=num_parqueaderos,
        estrato=estrato,

        genero_preferido=genero_preferido,
        permite_mascotas=permite_mascotas,
        permite_fumadores=permite_fumadores,
        permite_fiestas=permite_fiestas,

        fotos=",".join(rutas_imagenes)
    )

    db.add(inmueble)
    db.commit()
    db.refresh(inmueble)

    publicacion = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()
    if publicacion:
        publicacion.inmueble_id = inmueble.id
        db.commit()

    return RedirectResponse("/inicio?mensaje=publicacion_exitosa", status_code=302)
