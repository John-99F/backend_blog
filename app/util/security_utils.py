from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, ExpiredSignatureError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

passwordHasher = PasswordHasher()

SECRET_KEY = ""  # debes llenarlo con un valor seguro desde .env
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 1

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


# ----- JWT -----
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def expires_times():
    return timedelta(minutes=TOKEN_EXPIRE_MINUTES)


# OAuth2 (token bearer)
authToken = OAuth2PasswordBearer(tokenUrl="token")


# ----- VERIFICAR TOKEN -----
def verificar_token(token: str = Depends(authToken)):
    """
    Verifica y decodifica el token enviado en Authorization: Bearer <token>
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido o mal formado")

        return usuario

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
