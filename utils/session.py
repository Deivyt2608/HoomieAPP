from fastapi import Request
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import User
from typing import Optional

def get_usuario_logueado(request: Request) -> Optional[User]:
    usuario_email = request.cookies.get("usuario_email")
    if not usuario_email:
        return None

    db: Session = SessionLocal()
    usuario = db.query(User).filter(User.email == usuario_email).first()
    db.close()
    return usuario
