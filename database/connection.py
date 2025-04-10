from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:nyQKgoeRzwVQwXQWJpFJZGHknrbbKRdH@yamabiko.proxy.rlwy.net:39022/railway"  # Cambia según tu usuario y contraseña

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()