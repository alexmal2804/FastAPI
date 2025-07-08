from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models import User, UserInDB
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = [
    # {"username": "alex2", "hashed_password": pwd_context.hash("test_password")}
]

def get_user(username: str): 
    for user in fake_users_db:
        if user["username"] == username:  # Доступ через ключ словаря
            return user
    return None

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if user and pwd_context.verify(credentials.password, user["hashed_password"]):
        return UserInDB(**user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/login")
def login(user: UserInDB = Depends(authenticate_user)):
    return {"message": f"Welcome back! {user.username}"}


@app.get("/register")
def register(user: User = Depends(User)):
    if not user.username or not user.password:
        raise HTTPException(status_code=401, detail="Invalid user information")
    if user:
        userInDB = UserInDB(
            username=user.username, hashed_password=pwd_context.hash(user.password)
        )
        fake_users_db.append(userInDB)
        return {"message": "User registered successfully!", "user_info": fake_users_db}
    else:
        raise HTTPException(
            status_code=401,
            detail="User already exists or invalid user information",
            headers={"WWW-Authenticate": "Basic"},
        )
