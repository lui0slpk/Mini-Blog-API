
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.models.user import User

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRES_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autenticado",
    headers={"WWW-authenticate": "Bearer"}
)


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expirado",
        headers={"WWW-authenticate": "Bearer"}
    )


def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes"
    )


def invalid_credentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas"
    )

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.now(
#         tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))
#     to_encode.update({"exp": expire})
#     token = jwt.encode(
#         payload=to_encode,
#         key=JWT_SECRET_KEY,
#         algorithm=JWT_ALGORITHM
#     )

#     return token


def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=minutes or ACCESS_TOKEN_EXPIRES_MINUTES)

    return jwt.encode(
        payload={
            "sub": sub,
            "exp": expire
        },
        key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def decode_token(token: str) -> dict:
    playload = jwt.decode(
        jwt=token,
        key=JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM]
    )

    return playload


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:

    try:
        playload = decode_token(token)
        sub: str | None = playload.get("sub")
        username: str | None = playload.get("username")
        if not sub or not username:
            raise credentials_exc

        user_id = int(sub)
    except ExpiredSignatureError:
        raise raise_expired_token()
    except InvalidTokenError:
        raise credentials_exc
    except PyJWTError:
        raise invalid_credentials()

    user = db.get(User, user_id)

    if not user or not user.is_active:
        raise invalid_credentials()

    return user


def hashed_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def require_role(min_role: Literal["user", "editor", "admin"]) -> User:
    order = {
        "user": 0,
        "editor": 1,
        "admin": 2
    }

    def evaluation(user: User = Depends(get_current_user)) -> User:
        if order[user.role] < order[min_role]:
            raise raise_forbidden()

        return user

    return evaluation()


require_user = require_role("user")
require_editor = require_role("editor")
require_admin = require_role("admin")
