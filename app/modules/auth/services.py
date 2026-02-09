import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.users import services as user_services
from app.shared.utils.password import verify_password

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def authenticate_user(db: Session, email: str, password: str):
    user = user_services.get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if not user_id:
            return None
        return int(user_id)
    except InvalidTokenError:
        raise None
