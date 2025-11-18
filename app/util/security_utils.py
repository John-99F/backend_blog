from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException

import jwt
from jwt import InvalidTokenError
##CIFRADO DE CONTRASEÑA
passwordHasher = PasswordHasher()

SECRET_KEY = ""
ALGORITHM="HS256"
TOKEN_EXPIRE_MINUTES = 1


def get_password_hash(password: str) -> str:
    return passwordHasher.hash(password= password)

def verify_password(plain_password: str, hashed_password: str) -> str:
    try: 
        passwordHasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception:
        return False
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM )

def expires_times():
    return timedelta(minutes=TOKEN_EXPIRE_MINUTES)

authToken = OAuth2PasswordBearer(tokenUrl="token")


def verificar_token(token: str = Depends(authToken)):
    """
    Verifica el token JWT recibido en la cabecera Authorization.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return usuario
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
