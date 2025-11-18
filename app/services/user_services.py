from app.data.database import Base, engine, get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.data.models.users import User
from app.util.security_utils import verify_password, create_access_token, expires_times

#Servicio para crear o registrar usuarios
def create_user(name, surname, email, password, db: Session = Depends(get_db)):
    new_user = User(name= name, surname= surname, email = email, password= password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.to_dict()

#Servicio para realizar el login 
def login(email, password, db: Session = Depends(get_db)):
    statement = select(User).filter_by(email = email)
    user = db.scalars(statement).all()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail= "Datos incorrectos por favor revisar nuevamente.")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail= "Datos incorrectos por favor revisar nuevamente.")
    access_token = create_access_token(
        data={"sub": email},
        expires_delta= expires_times
    )

    return {
        "status":"success",
        "mensaje": "Login exitoso",
        "token":access_token,
        "token_type":"bearer"
    }