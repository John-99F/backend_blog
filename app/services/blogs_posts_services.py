from app.data.database import Base, engine, get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.services.google_services import generar_blog
from app.data.models.articles import Article
import json


def get_all_post(db:  Session = Depends(get_db)): 
    articles = db.query(Article).all()
    db.close()
    return [a.to_dict() for a in articles]


def generate_post(prompt,
                  current_user,
                  db: Session = Depends(get_db),):

    # 1. Generar artículo con IA
    result = generar_blog(prompt)

    try:
        json_data = json.loads(result)
    except:
        raise HTTPException(status_code=500, detail="La IA no devolvió un JSON válido")

    # 2. Guardar en BD
    post = Article(
        title=json_data["title"],
        description=json_data["description"],
        imageurl=json_data["imageurl"],
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
