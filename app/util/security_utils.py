from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException
from dotenv import load_dotenv
import jwt
from jwt import InvalidTokenError
import os

load_dotenv()

passwordHasher = PasswordHasher()

SECRET_KEY = "secreto"
ALGORITHM = "HS256"


# ------------------------------
# HASH PASSWORD
# ------------------------------
def hash_password(password: str) -> str:
    return passwordHasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        passwordHasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


# ------------------------------
# EXPIRACIÓN DEL TOKEN
# ------------------------------
def expires_times(minutes: int = 30):
    """Retorna el tiempo de expiración"""
    return timedelta(minutes=minutes)


# ------------------------------
# CREAR TOKEN JWT
# ------------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crea un token JWT con expiración"""

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# ------------------------------
# VERIFICAR TOKEN
# ------------------------------
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o corrupto")
