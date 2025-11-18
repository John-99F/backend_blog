from app.data.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.data.models.users import User
from app.util.security_utils import verify_password, create_access_token, expires_times


# Crear usuario
def create_user(name, surname, email, password, db: Session = Depends(get_db)):
    existing = db.scalars(select(User).filter_by(email=email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    new_user = User(
        name=name,
        surname=surname,
        email=email,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user.to_dict()


# Login
def login(email, password, db: Session = Depends(get_db)):
    statement = select(User).filter_by(email=email)
    user = db.scalars(statement).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Datos incorrectos por favor revisar nuevamente."
        )

    # Verificar contraseña
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Datos incorrectos por favor revisar nuevamente."
        )

    # Crear token
    access_token = create_access_token(
        data={"sub": user.id},   # Usar ID del usuario
        expires_delta=expires_times()
    )

    return {
        "status": "success",
        "mensaje": "Login exitoso",
        "token": access_token,
        "token_type": "bearer"
    }
