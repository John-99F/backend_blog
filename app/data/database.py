from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.util.parameters import DATABASE_URL 

#Archivo para crear la base de datos
engine = create_engine(str(DATABASE_URL), echo= True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit= False)

Base = declarative_base()