from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:WGUEuZYpIsEWIvpTRHQIzFTbkrXNBijb@shinkansen.proxy.rlwy.net:10299/railway"  # Cambia según tu usuario y contraseña
#DATABASE_URL = "mysql+pymysql://root:@localhost/hoomie"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
