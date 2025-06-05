# routers/publicacion.py
from fastapi import APIRouter, Form, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.publicacion import Publicacion
from models.inmueble import Inmueble
from models.user import User
import shutil, os
import uuid
from utils.session import get_usuario_logueado

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

@router.post("/editar-publicacion/{publicacion_id}")
def editar_publicacion(
    publicacion_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    tipo_publicacion: str = Form(...),
    tipo_inmueble: str = Form(...),
    ciudad: str = Form(...),
    barrio: str = Form(...),
    direccion: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    valor_arriendo: int = Form(...),
    valor_administracion: int = Form(None),
    area_m2: int = Form(...),
    num_banos: int = Form(...),
    num_habitaciones: int = Form(...),
    num_parqueaderos: int = Form(...),
    estrato: int = Form(...),
    genero_preferido: str = Form(...),
    permite_mascotas: bool = Form(...),
    permite_fumadores: bool = Form(...),
    permite_fiestas: bool = Form(...),
    fotos: list[UploadFile] = File(None),
    db: Session = Depends(get_db),
    usuario_logueado: User = Depends(get_usuario_logueado)
):
    publicacion = db.query(Publicacion).filter(Publicacion.id == publicacion_id).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    if publicacion.usuario_id != usuario_logueado.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Actualiza campos
    publicacion.nombre = nombre
    publicacion.descripcion = descripcion
    publicacion.tipo_publicacion = tipo_publicacion

    inmueble = publicacion.inmueble
    inmueble.tipo_inmueble = tipo_inmueble
    inmueble.ciudad = ciudad
    inmueble.barrio = barrio
    inmueble.direccion = direccion
    inmueble.latitud = latitud
    inmueble.longitud = longitud
    inmueble.valor_arriendo = valor_arriendo
    inmueble.valor_administracion = valor_administracion
    inmueble.area_m2 = area_m2
    inmueble.num_banos = num_banos
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_parqueaderos = num_parqueaderos
    inmueble.estrato = estrato
    inmueble.genero_preferido = genero_preferido
    inmueble.permite_mascotas = permite_mascotas
    inmueble.permite_fumadores = permite_fumadores
    inmueble.permite_fiestas = permite_fiestas

    # Fotos (si se suben nuevas)
    if fotos:
        nombres_fotos = []
        for foto in fotos:
            extension = os.path.splitext(foto.filename)[1]
            nombre_archivo = f"{uuid.uuid4().hex}{extension}"
            ruta = f"static/fotos/{nombre_archivo}"
            with open(ruta, "wb") as buffer:
                shutil.copyfileobj(foto.file, buffer)
            nombres_fotos.append(ruta)
        inmueble.fotos = ",".join(nombres_fotos)

    db.commit()
    return RedirectResponse(f"/detalle/{publicacion.id}?mensaje=editado", status_code=303)
