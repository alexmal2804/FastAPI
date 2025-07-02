# main.py
from fastapi import FastAPI


app = FastAPI()

# Пример файковой БД
fake_users = {
    1: {"username": "Alex", "age": 20, "email": "alex@gmail.com "},
    2: {"username": "John", "age": 21, "email": "john@gmail.com"},
    3: {"username": "Jane", "age": 22, "email": "jane@gmail.com"},
    4: {"username": "Jim", "age": 23, "email": "jim@gmail.com"},
    5: {"username": "Jill", "age": 24, "email": "jill@gmail.com"},
    6: {"username": "Jack", "age": 25, "email": "jack@gmail.com"},
    7: {"username": "Jill", "age": 26, "email": "jill@gmail.com"},
    8: {"username": "Jill", "age": 27, "email": "jill@gmail.com"},
    9: {"username": "Jill", "age": 28, "email": "jill@gmail.com"},
    10: {"username": "Jill", "age": 29, "email": "jill@gmail.com"},
}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}
