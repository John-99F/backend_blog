from fastapi import FastAPI
from app.data.database import Base, engine

# Importa los routers *correctos* desde los módulos
from app.controller.user_controller import router as user_router
from app.controller.blogs_posts_controller import router as blogs_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend Blog IA",
        description="Trabajo final backend",
        version="1.0.0"
    )

    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    # Incluir routers correctos
    app.include_router(user_router)
    app.include_router(blogs_router)

    return app


app = create_app()
