from fastapi import APIRouter, HTTPException, Body, Depends
from app.services.blogs_posts_services import get_all_post, generate_post
from app.util.security_utils import verificar_token

router = APIRouter(prefix="/blog", tags=["Blog"])


# Obtener todos los posts
@router.get("/posts")
def get_posts():
    try:
        return get_all_post()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generar un post usando IA (requiere token)
@router.post("/generate-post")
def create_post(
    prompt_data: dict = Body(...),
    token: str = Depends(verificar_token)
):
    try:
        if "prompt" not in prompt_data:
            raise HTTPException(status_code=422, detail="El campo 'prompt' es obligatorio")

        response = generate_post(prompt_data["prompt"])

        return {
            "status": "success",
            "data": response
        }

    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))
