import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables .env en local
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise Exception("DB_URL no está configurado en variables de entorno")

# Render usa "postgres://" → SQLAlchemy requiere "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # evita desconexiones cuando Render "duerme"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Obtener sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
