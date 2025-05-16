# scripts/generar_apartamentos.py
from database.connection import SessionLocal
from models.inmueble import Inmueble
from models.user import User
from models.publicacion import Publicacion
import random

ciudades = ["Bogotá", "Medellín", "cartagena"]
barrio_base = ["Chapinero", "Laureles", "San Fernando", "El Prado"]
tipos = ["apartamento", "casa"]
generos = ["masculino", "femenino", "indiferente"]

fotos_base = "/static/imagenes/apartamentos/demo1.jpg,/static/imagenes/apartamentos/demo2.jpg"

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

    # Crear 10 inmuebles y publicaciones asociadas
    for i in range(10):
        ciudad = random.choice(ciudades)
        barrio = random.choice(barrio_base)
        tipo = random.choice(tipos)
        genero = random.choice(generos)
        precios = random.choice(valores)
        usuario = random.choice(usuarios)

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
            fotos=fotos_base
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
