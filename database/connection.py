from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgreql://postgres:Santi124.@db.zvrpmagggxufaqcaitic.supabase.co:5432/postgres"  # Cambia según tu usuario y contraseña
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
