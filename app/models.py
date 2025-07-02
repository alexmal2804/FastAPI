import random

from pydantic import BaseModel


class User(BaseModel):
    name: str
    id: int = random.randint(1, 1000)
    age: int = 18
