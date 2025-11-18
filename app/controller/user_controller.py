from fastapi import APIRouter, HTTPException, Body
from app.services.user_services import  create_user, login
from app.util.security_utils import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])

#Controlador que crea los usuarios - POST 
@router.post("/register")
def post_user(user_data: dict = Body(...)):
    try: 
        hashed_password = get_password_hash(user_data["password"])
        new_user = create_user( 
            user_data["name"],
            user_data["surName"],
            user_data["email"],
            hashed_password
        )
        return {"status":"success" , "data":new_user}
    except Exception as exception: 
        raise HTTPException(status_code=400, detail=str(exception))
    

# Controlador que busca usuario por email y contraseña - POST
@router.post("/token")
def login_user(credentials: dict = Body(...)):
    try:
        user = login(credentials["email"], credentials["password"])
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
