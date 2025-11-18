from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from app.services.user_services import create_user, login
from app.util.security_utils import get_password_hash
from app.data.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# Registrar usuario
@router.post("/register")
def post_user(user_data: dict = Body(...), db: Session = Depends(get_db)):
    try:
        if "password" not in user_data:
            raise HTTPException(status_code=422, detail="La contraseña es obligatoria")

        hashed_password = get_password_hash(user_data["password"])

        new_user = create_user(
            user_data["name"],
            user_data["surName"],
            user_data["email"],
            hashed_password,
            db
        )

        return {"status": "success", "data": new_user}

    except Exception as exception:
        raise HTTPException(status_code=400, detail=str(exception))


# Login
@router.post("/token")
def login_user(credentials: dict = Body(...), db: Session = Depends(get_db)):
    try:
        if "email" not in credentials or "password" not in credentials:
            raise HTTPException(status_code=422, detail="Email y password requeridos")

        user = login(credentials["email"], credentials["password"], db)

        return user

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
