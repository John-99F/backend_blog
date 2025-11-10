from fastapi import FastAPI
from app.data.database import Base, engine


app = FastAPI(
    title="Backend Blog IA",
    description="Trabajo final backend",
    version="1.0.0"
)


#Crea la base de datos 
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    print("Servidor corriendo en http://localhost:8080")
    uvicorn.run("app.main:app",host="0.0.0.0", port=8080, reload=True)