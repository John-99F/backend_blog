from app.data.database import Base, engine, get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.services.google_services import generar_blog
from app.data.models.articles import Article
import json


def get_all_post(db: Session = Depends(get_db)): 
    articles = db.query(Article).all()
    return [a.to_dict() for a in articles]


def generate_post(
    prompt: str,
    current_user: str,     # ID o email del usuario extraído del JWT
    db: Session = Depends(get_db)
):

    # 1. Llamar API de IA
    result = generar_blog(prompt)

    # 2. Validar JSON que devuelve Gemini
    try:
        json_data = json.loads(result)
    except Exception:
        raise HTTPException(
            status_code=500, 
            detail="La IA no devolvió un JSON válido"
        )

    # 3. Guardar artículo en BD
    post = Article(
        title=json_data.get("title"),
        description=json_data.get("description"),
        imageurl=json_data.get("imageurl"),
        author_id=current_user  # viene del token JWT
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
