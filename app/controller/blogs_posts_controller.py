from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from app.services.blogs_posts_services import get_all_post, generate_post
from app.util.security_utils import verificar_token
from app.data.database import get_db

router = APIRouter(prefix="/blog", tags=["Blog"])


# Obtener todos los posts
@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    try:
        return get_all_post(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generar un post usando IA (requiere token)
@router.post("/generate-post")
def create_post(
    prompt_data: dict = Body(...),
    current_user: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    try:
        if "prompt" not in prompt_data:
            raise HTTPException(status_code=422, detail="El campo 'prompt' es obligatorio")

        response = generate_post(prompt_data["prompt"], current_user, db)

        return {
            "status": "success",
            "data": response
        }

    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))
