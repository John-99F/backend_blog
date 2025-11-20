from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data.database import Base, engine

# Routers
from app.controller.user_controller import router as user_router
from app.controller.blogs_posts_controller import router as blogs_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend Blog IA",
        description="Trabajo final backend",
        version="1.0.0"
    )

    # CORS CONFIG
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://backend-blog-snpc.onrender.com",
        "*"  # permitir todo mientras pruebas
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],      # GET, POST, PUT, DELETE, OPTIONS
        allow_headers=["*"],      # Authorization, Content-Type, etc.
    )

    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Rutas
    app.include_router(user_router)
    app.include_router(blogs_router)

    return app


app = create_app()
