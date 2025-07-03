# main.py
from fastapi import FastAPI

from .models import Feedback, User1


app = FastAPI()

# Пример файковой БД
fake_users: User1 = [
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

fake_feedbacks: Feedback = []


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
        filtered_users = [user for user in fake_users if user["username"].lower() == username.lower()]
    if email:
        filtered_users = [user for user in filtered_users if user["email"].lower() == email.lower()]
    return filtered_users[:limit]


@app.get("/all_users")
def read_all_users():
    return fake_users


@app.post("/add_user", response_model=User1)
async def add_user(user: User1):
    fake_users.append({"username": user.username, "age": user.age, "email": user.email})
    return user


@app.post("/feedback")
async def add_feedback(feedback: Feedback):
    fake_feedbacks.append({"name": feedback.name, "message": feedback.message})
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв принят."}
