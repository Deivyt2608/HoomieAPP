import aiosmtplib
from email.message import EmailMessage

async def enviar_correo_bienvenida(destinatario: str, nombre: str):
    mensaje = EmailMessage()
    mensaje["From"] = "hoomieapp2609@gmail.com"
    mensaje["To"] = destinatario
    mensaje["Subject"] = "¡Bienvenido a Hoomie!"
    
    mensaje.set_content(f"""
Hola {nombre},

¡Gracias por registrarte en Hoomie! 🏡✨

Ya puedes empezar a buscar tu roomie o compartir tu espacio con otros.

Saludos,
El equipo de Hoomie
    """)

    await aiosmtplib.send(
        mensaje,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="hoomieapp2609@gmail.com",
        password="qdny bsda jtrm khes"
    )

async def enviar_enlace_restablecer(correo: str, nombre: str, enlace: str):
    mensaje = EmailMessage()
    mensaje["From"] = "hoomieapp2609@gmail.com"
    mensaje["To"] = correo
    mensaje["Subject"] = "Restablece tu contraseña"
    mensaje.set_content(f"""
Hola {nombre},

Haz clic en este enlace para restablecer tu contraseña:
{enlace}

Si no solicitaste esto, ignora este mensaje.
""")

    await aiosmtplib.send(
        mensaje,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="hoomieapp2609@gmail.com",
        password="qdny bsda jtrm khes"
    )
