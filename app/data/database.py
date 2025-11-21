import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# IMPORTAR TU MODELO
from app.data.models.articles import Article  # 👈 IMPORTANTE

Base = declarative_base()

# Detectar si estamos en producción (Render aplica DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (Render)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True
    )

    print("🔵 Usando PostgreSQL (Render/Producción)")

else:
    # SQLite (Local)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./blogDb.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    print("🟢 Usando SQLite (Local)")


# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# 🚨 NUEVO: Función para eliminar y recrear la tabla Article
def recreate_article_table():
    print("⚠ Eliminando tabla Article si existe...")
    Article.__table__.drop(engine, checkfirst=True)

    print("🛠 Creando tabla Article...")
    Article.__table__.create(engine)

    print("✅ Tabla Article recreada correctamente.")


# Ejecutar directamente desde Python
if __name__ == "__main__":
    recreate_article_table()
