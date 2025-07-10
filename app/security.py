from typing import Optional
import jwt
import datetime
from fastapi import Depends
from .db import USERS_DATA
from .models import UserWithData, UserLogin
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext    
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import logging

security = HTTPBasic()

logger = logging.getLogger("jwt_debug")
logger.setLevel(logging.DEBUG)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Function to create a JWT token
def create_jwt_token(user: UserLogin):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.username,
        "exp": expiration
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_user(username: str) -> Optional[UserLogin]:
    for user_dict in USERS_DATA:
        user = UserLogin(**user_dict)  # Преобразование словаря в объект UserLogin
        if user.username == username:
            return user
    return None
    

# Function to get user data from the fake database
def get_user_from_token(token: str = Depends(oauth2_scheme)) -> Optional[UserLogin]:
    try:
        logger.debug(f"Decoding token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded payload: {payload}")
        username = payload.get("sub")
        if username:
            return username
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.ExpiredSignatureError as e:
       logger.error(f"Expired token error: {e}")
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user_data = get_user(credentials.username) 
    if user_data and pwd_context.verify(credentials.password, user_data.password):
        return user_data
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    ) 