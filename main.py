from fastapi import FastAPI
from app.data.database import Base, engine
from app.controller import user_controller, blogs_posts_controller

def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend Blog IA",
        description="Trabajo final backend",
        version="1.0.0"
    )

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(user_controller)
    app.include_router(blogs_posts_controller)

    return app

app = create_app()