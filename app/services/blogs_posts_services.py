from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.google_services import generar_blog
from app.data.models.articles import Article
import json


def get_all_post(db: Session):
    articles = db.query(Article).all()
    return [a.to_dict() for a in articles]


def generate_post(prompt: str, current_user: str, db: Session):

    # 1. Generar contenido con IA
    result = generar_blog(prompt)
    print(f"json: {result}")

    # 2. Validar JSON
    try:
        json_data = json.loads(result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"La IA no devolvió un JSON válido {e}"
        )

    # 3. Crear artículo (AJUSTE DE CLAVES)
    post = Article(
        id=json_data.get("id"),
        title=json_data.get("title"),
        description=json_data.get("description"),
        image_url=json_data.get("imageurl"),  # <---- AJUSTE
        date_creation=json_data.get("datecreation"),  # <---- AJUSTE
        autor_id=current_user  # <---- AJUSTADO
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    # 4. Retornar correctamente
    return {
        "message": "Artículo generado y guardado correctamente",
        "post": {
            "id": post.id,
            "title": post.title,
            "autor_id": post.autor_id,
            "image_url": post.image_url,
        }
    }
