from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config.settings import settings


ALGORITHM = "HS256"


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )
    
from jose import JWTError

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        raise ValueError("Invalid token")    
    