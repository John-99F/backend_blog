from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from dotenv import load_dotenv

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

# Cargar variables de entorno
load_dotenv()

passwordHasher = PasswordHasher()

# Usa una llave real
SECRET_KEY = "mi_llave_super_secreta"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 5


# ----- HASH DE CONTRASEÑA -----
def get_password_hash(password: str) -> str:
    return passwordHasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        passwordHasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception:
        return False


# ----- CREAR TOKEN -----
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Siempre incluir sub, obligatorio para identificación
    if "sub" not in to_encode:
        raise ValueError("El token debe incluir el campo 'sub'")

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("DEBUG TOKEN GENERADO:", token)
    return token


# ----- OAuth2 -----
authToken = OAuth2PasswordBearer(tokenUrl="/users/token")


# ----- VERIFICAR TOKEN -----
def verificar_token(token: str = Depends(authToken)):
    """
    Verifica el token JWT recibido en la cabecera Authorization.
    """
    print("DEBUG TOKEN RECIBIDO:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("DEBUG PAYLOAD:", payload)

        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")

        return usuario

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o corrupto")

    except Exception as e:
        print("DEBUG ERROR INESPERADO:", e)
        raise HTTPException(status_code=401, detail="Token inválido")
