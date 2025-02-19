from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError

from schemas.settings import Settings

auth_schema = OAuth2PasswordBearer(tokenUrl='/api/auth/token')
settings = Settings()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(auth_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.JWT_ALGORITHM])
        username: str = payload.get('username')
        if username is None:
            raise credentials_exception

        user = {
            'username': username,
        }

    except InvalidTokenError:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user
