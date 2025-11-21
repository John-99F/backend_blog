import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.google_services import generar_blog
from app.data.models.articles import Article


def get_all_post(db: Session):
    articles = db.query(Article).all()
    return [a.to_dict() for a in articles]


def generate_post(prompt: str, current_user: str, db: Session):

    # 1. Generar contenido
    result = generar_blog(prompt)
    print("IA RAW:", result)

    # 2. Convertir a JSON correctamente
    try:
        if isinstance(result, dict):
            # La IA ya devolvió JSON como diccionario
            json_data = result
        else:
            # Es un string → entonces se parsea
            json_data = json.loads(result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"La IA no devolvió un JSON válido: {e}"
        )

    # 3. Crear artículo
    post = Article(
        id=json_data.get("id"),
        title=json_data.get("title"),
        description=json_data.get("description"),
        image_url=json_data.get("imageurl"),       # 👈 mapeo correcto
        date_creation=json_data.get("datecreation"),
        autor_id=current_user                      # 👈 tu modelo usa autor_id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {
        "message": "Artículo generado y guardado correctamente",
        "post": post.to_dict()
    }
