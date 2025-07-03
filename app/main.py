# main.py
from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    age: int
    email: str


app = FastAPI()

# Пример файковой БД
fake_users = [
    {"username": "Alex", "age": 20, "email": "alex@gmail.com "},
    {"username": "John", "age": 21, "email": "john@gmail.com"},
    {"username": "Jane", "age": 22, "email": "jane@gmail.com"},
    {"username": "Jim", "age": 23, "email": "jim@gmail.com"},
    {"username": "Jill", "age": 24, "email": "jill@gmail.com"},
    {"username": "Jack", "age": 25, "email": "jack@gmail.com"},
    {"username": "Bob", "age": 26, "email": "bob@gmail.com"},
    {"username": "Alice", "age": 27, "email": "alice@gmail.com"},
    {"username": "Charlie", "age": 28, "email": "charlie@gmail.com"},
    {"username": "Diana", "age": 29, "email": "diana@gmail.com"},
    {"username": "Eve", "age": 30, "email": "eve@gmail.com"},
    {"username": "Frank", "age": 31, "email": "frank@gmail.com"},
    {"username": "George", "age": 32, "email": "george@gmail.com"},
    {"username": "Hannah", "age": 33, "email": "hannah@gmail.com"},
    {"username": "Isaac", "age": 34, "email": "isaac@gmail.com"},
    {"username": "Julia", "age": 35, "email": "julia@gmail.com"},
    {"username": "Kevin", "age": 36, "email": "kevin@gmail.com"},
    {"username": "Liam", "age": 37, "email": "liam@gmail.com"},
    {"username": "Mia", "age": 38, "email": "mia@gmail.com"},
    {"username": "Jack", "age": 17, "email": "jack17@gmail.com"},
]


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.get("/limit")
def read_users_limit(limit: int = 10, offset: int = 0):
    return dict(list(fake_users.items())[offset : offset + limit])


@app.get("/users")
def read_users(username: str = None, email: str = None, limit: int = 10):
    filtered_users = fake_users
    if username:
        filtered_users = {key: user for key, user in fake_users.items() if user["username"].lower() == username.lower()}
    if email:
        filtered_users = {key: user for key, user in fake_users.items() if user["email"].lower() == email.lower()}
    return dict(list(filtered_users.items())[:limit])


@app.get("/all_users")
def read_all_users():
    return fake_users


@app.post("/add_user", response_model=User)
async def add_user(user: User):
    fake_users.append({"username": user.username, "age": user.age, "email": user.email})
    return user  # {"message": f"Пользователь {user} успешно добавлен в базу данных"}
