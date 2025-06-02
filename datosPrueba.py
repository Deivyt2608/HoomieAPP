from database.connection import SessionLocal
from models.inmueble import Inmueble
from models.user import User
from models.publicacion import Publicacion
from models.preferencias import Preference
import random
from database.connection import Base, engine

print("⚠ ATENCIÓN: Eliminando todas las tablas...")
Base.metadata.drop_all(bind=engine)
print("✅ Tablas eliminadas.")

print("🔧 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")

# Ciudades y barrios asociados
ciudades_barrios = {
    "Bogotá": ["Chapinero", "Usaquén", "Teusaquillo"],
    "Medellín": ["Laureles", "El Poblado", "Belén"],
    "Cartagena": ["San Diego", "Getsemaní", "Bocagrande"]
}

tipos = ["apartamento", "casa"]
generos = ["masculino", "femenino", "indiferente"]
tipos_publicacion = ["arrendar", "buscar roomie"]

nombres_publicacion = [
    "Arriendo habitación amoblada",
    "Se busca roomie responsable",
    "Habitación disponible zona céntrica",
    "Compartir apartamento amplio",
    "Arriendo cuarto independiente"
]

descripciones = [
    "Espacio cómodo y tranquilo, ideal para estudiantes o profesionales.",
    "Habitación iluminada, acceso a cocina y zonas comunes.",
    "A pocos minutos del transporte público y universidades.",
    "Ambiente amigable, incluye servicios y wifi.",
    "Con opción a parqueadero y servicios incluidos."
]

valores = [
    {"arriendo": 900000, "admin": 120000},
    {"arriendo": 1200000, "admin": 200000},
    {"arriendo": 700000, "admin": 0},
    {"arriendo": 1500000, "admin": 180000},
    {"arriendo": 1000000, "admin": 150000}
]

def generar_apartamentos_con_usuarios():
    db = SessionLocal()

    # Crear 3 usuarios de prueba
    usuarios = []
    for i in range(3):
        user = User(
            nombre=f"Usuario{i+1}",
            apellido="Prueba",
            email=f"usuario{i+1}@hoomie.com",
            password="12345",
            phone=f"30000000{i+1}",
            foto=""
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        usuarios.append(user)

        preferencia = Preference(
            user_id=user.id,
            aseo_hogar=random.randint(1, 5),
            ruido_hogar=random.randint(1, 5),
            visitas=random.randint(1, 5),
            aseo_personal=random.randint(1, 5),
            division_tareas=random.randint(1, 5),
            salidas_fiesta=random.randint(1, 5),
            fuma=random.choice(["sí", "no"]),
            alcohol=random.choice(["sí", "no"]),
            trabaja_casa=random.choice(["sí", "no"]),
            mascotas=random.choice(["sí", "no"]),
            estudia=random.choice(["sí", "no"]),
            trabaja=random.choice(["sí", "no"])
        )
        db.add(preferencia)

    # Generar lista única de imágenes demo1.jpg a demo10.jpg
    imagenes = [f"/static/imagenes/apartamentos/demo{i+1}.jpg" for i in range(10)]
    random.shuffle(imagenes)

    # Crear 10 inmuebles y publicaciones asociadas
    for i in range(10):
        ciudad = random.choice(list(ciudades_barrios.keys()))
        barrio = random.choice(ciudades_barrios[ciudad])
        tipo = random.choice(tipos)
        genero = random.choice(generos)
        precios = random.choice(valores)
        usuario = random.choice(usuarios)
        imagen = imagenes.pop()  # sacar una imagen única

        inmueble = Inmueble(
            tipo_inmueble=tipo,
            direccion=f"Calle {random.randint(1,100)} #{random.randint(1,50)}-{random.randint(1,20)}",
            barrio=barrio,
            ciudad=ciudad,
            valor_arriendo=precios["arriendo"],
            valor_administracion=precios["admin"],
            area_m2=random.randint(35, 100),
            num_habitaciones=random.randint(1, 4),
            num_banos=random.randint(1, 3),
            num_parqueaderos=random.randint(0, 2),
            estrato=random.randint(2, 6),
            genero_preferido=genero,
            permite_mascotas=random.choice([True, False]),
            permite_fumadores=random.choice([True, False]),
            permite_fiestas=random.choice([True, False]),
            fotos=imagen  # solo una imagen
        )
        db.add(inmueble)
        db.commit()
        db.refresh(inmueble)

        publicacion = Publicacion(
            nombre=random.choice(nombres_publicacion),
            descripcion=random.choice(descripciones),
            tipo_publicacion=random.choice(tipos_publicacion),
            usuario_id=usuario.id,
            inmueble_id=inmueble.id
        )
        db.add(publicacion)

    db.commit()
    db.close()
    print("✅ Se generaron usuarios, inmuebles y publicaciones de prueba.")

if __name__ == "__main__":
    generar_apartamentos_con_usuarios()
