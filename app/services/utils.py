from datetime import datetime, timezone, timedelta
import time

import jwt
from jose import JWTError
from models.user import UserClaims
from entities.user import User
from settings import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from services.exception import UnAuthorizedError

def get_current_utc_time() -> datetime:
    return datetime.now(timezone.utc)

def get_current_timestamp() -> int:
    return int(time.time())

def create_access_token(user: User, expires: int = None):

    claims = UserClaims(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        email_verified=True,
        first_name=user.first_name,
        last_name=user.last_name,
        is_admin=user.is_admin,
        aud='FastAPI',
        iss='FastAPI',
        iat=get_current_timestamp(),
        exp=get_current_timestamp() + expires if expires else get_current_timestamp() + int(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
    )
    
    
    token = jwt.encode(claims.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience='FastAPI', issuer='FastAPI')
        return payload
    except JWTError:
        raise UnAuthorizedError("Invalid token")