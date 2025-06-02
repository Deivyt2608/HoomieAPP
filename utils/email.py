import aiosmtplib
from email.message import EmailMessage

async def enviar_correo_bienvenida(destinatario: str, nombre: str):
    mensaje = EmailMessage()
    mensaje["From"] = "hoomieapp2609@gmail.com"
    mensaje["To"] = destinatario
    mensaje["Subject"] = "¡Bienvenido a Hoomie!"
    
    # Parte HTML
    html_content = f"""
    <html>
      <body>
        <h2>¡Hola {nombre}!</h2>
        <p>🏡✨ ¡Gracias por registrarte en <b>Hoomie</b>! 🏡✨</p>
        <p>Ya puedes empezar a buscar tu roomie o compartir tu espacio con otros.</p>
        <img src="https://res.cloudinary.com/df7elploy/image/upload/v1748900325/correo_maqmx1.png" alt="Correo Bienvenida" width="400" style="margin-top:20px;">
        <p>Saludos,<br>El equipo de Hoomie</p>
      </body>
    </html>
    """

    mensaje.set_content(f"""
Hola {nombre},

¡Gracias por registrarte en Hoomie!

Ya puedes empezar a buscar tu roomie o compartir tu espacio con otros.

Saludos👋,
El equipo de Hoomie 💙💛
    """)  # Texto alternativo (para clientes que no leen HTML)
    
    mensaje.add_alternative(html_content, subtype='html')

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
    
    # Parte HTML
    html_content = f"""
    <html>
      <body>
        <h2>Hola {nombre},</h2>
        <p>🔑 Hemos recibido una solicitud para restablecer tu contraseña.</p>
        <p>Puedes hacerlo haciendo clic en el siguiente enlace:</p>
        <p><a href="{enlace}" style="display:inline-block; padding:10px 20px; background-color:#FFC875; color:#000; text-decoration:none; border-radius:5px;">Restablecer contraseña</a></p>
        <img src="https://res.cloudinary.com/df7elploy/image/upload/v1748904079/restablece_txxr1v.png" alt="Restablecer Contraseña" width="400" style="margin-top:20px;">
        <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
        <p>Saludos,<br>El equipo de Hoomie 💙💛</p>
      </body>
    </html>
    """

    mensaje.set_content(f"""
Hola {nombre},

Haz clic en este enlace para restablecer tu contraseña:
{enlace}

Si no solicitaste esto, ignora este mensaje.

Saludos,
El equipo de Hoomie 💙💛
    """)  # Texto alternativo

    mensaje.add_alternative(html_content, subtype='html')

    await aiosmtplib.send(
        mensaje,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="hoomieapp2609@gmail.com",
        password="qdny bsda jtrm khes"
    )
