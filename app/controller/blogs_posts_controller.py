from fastapi import APIRouter, HTTPException, Body, Depends
from app.services.blogs_posts_services import  get_all_post, generate_post
from app.util.security_utils import verificar_token


router = APIRouter(prefix="/blog", tags=["Blog"])

@router.get("/posts")
def get_posts():
    articles = get_all_post()
    return articles

@router.post("/generate-post")
def create_post(promt: dict = Body(...),  token: str = Depends(verificar_token)):
    try: 
        response = generate_post(promt["prompt"])
        return {"status":"success", "data":response}
    except Exception as exception:
        raise HTTPException(status_code=400, detail= str(exception))