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
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="La IA no devolvió un JSON válido"
        )

    # 3. Crear artículo
    post = Article(
        title=json_data.get("title"),
        description=json_data.get("description"),
        imageurl=json_data.get("imageurl"),
        author_id=current_user
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {
        "message": "Artículo generado y guardado correctamente",
        "post": {
            "id": post.id,
            "title": post.title,
            "author_id": post.author_id,
            "imageurl": post.imageurl,
        }
    }
