from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response, Cookie

from .models import LoginInput

from itsdangerous import URLSafeTimedSerializer

app = FastAPI()

fake_user_db = [
    {"user123": {
        "username": "user123",
        "password": "password123",
    }},
    {"user456": {
        "username": "user456",
        "password": "password456",
    }},
    {"user789": {
        "username": "user789",
        "password": "password789",
    }},
    {"user101": {
        "username": "user101",
        "password": "password101",
    }}
]

session_store = {}

token_serializer = URLSafeTimedSerializer(secret_key="secret")  # Простой сериализатор для токена

# 🚪 /login: проверка логина и установка cookie
@app.post("/login")
def login(data: LoginInput, response: Response):
    for user_dict in fake_user_db:  # Итерируем по списку
        for _, person in user_dict.items():  # Извлекаем вложенные словари
            if person["username"] == data.username and person["password"] == data.password: 
                session_token = token_serializer.dumps(person)
                session_store[session_token] = person
                response.set_cookie(key="session_token", value=session_token, httponly=True)
                return {"session_token": session_token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# 🔒 /user: защищенный маршрут
@app.get("/user")
def get_user(session_token: str = Cookie(None)):
    user = token_serializer.loads(session_token, max_age=3600) if session_token else None
    if user:
        return user
    return {"message": "Unauthorized"}


# ❌ /logout: выход из системы
@app.post("/logout")
def logout(
    request: Request,
    response: Response,
):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        session_store.pop(session_token, None)
        # Удаляем cookie
        response.delete_cookie("session_token", path="/")
    return {"message": "Logout successful"}
