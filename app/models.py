from pydantic import BaseModel
import random


class User(BaseModel):
    name: str
    id: int = random.randint(1, 1000)
    age: int = 18   
