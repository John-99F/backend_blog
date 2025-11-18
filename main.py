from fastapi import FastAPI
from app.data.database import Base, engine
from app.controller import user_controller, blogs_posts_controller

app = FastAPI(
    title="Backend Blog IA",
    description="Trabajo final backend",
    version="1.0.0"
)


#Crea la base de datos 
Base.metadata.create_all(bind=engine)


app.include_router(user_controller)
app.include_router(blogs_posts_controller)


if __name__ == "__main__":
    import uvicorn
    print("Servidor corriendo en http://localhost:8080")
    uvicorn.run("app.main:app",host="0.0.0.0", port=8080, reload=True)