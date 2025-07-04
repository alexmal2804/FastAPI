from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response

from .models import LoginInput


app = FastAPI()

fake_user_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com",
        "full_name": "John Doe",
    }
}

session_store = {}


# 🚪 /login: проверка логина и установка cookie
@app.post("/login")
def login(data: LoginInput, response: Response):
    user = fake_user_db.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    session_token = str(uuid4())
    user["session_token"] = session_token
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,  # Cookie valid for 1 hour
        path="/",
    )
    return {"message": "Login successful"}


# 🔒 /user: защищенный маршрут
@app.get("/user")
def get_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = session_store.get(session_token)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = fake_user_db.get(username)
    return {
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
    }


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
