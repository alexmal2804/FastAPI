import inspect
import random
import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing_extensions import Annotated


# Патч для исправления проблемы с pymorphy2 в Python 3.13
if not hasattr(inspect, "getargspec"):

    def getargspec(func):
        spec = inspect.getfullargspec(func)
        return spec.args, spec.varargs, spec.varkw, spec.defaults

    inspect.getargspec = getargspec

from pymorphy2 import MorphAnalyzer


# Список недопустимых слов в начальной форме
bad_words = {"редиска", "бяка", "козявка"}

# Морфоанализатор
morph = MorphAnalyzer()


def contains_bad_words(text):
    words = re.findall(r"\b\w+\b", text.lower())
    for word in words:
        normal_form = morph.parse(word)[0].normal_form
        if normal_form in bad_words:
            return True
    return False


class User(BaseModel):
    name: str
    id: int = random.randint(1, 1000)
    age: int = 18


class User1(BaseModel):
    id: int
    username: str
    age: int
    email: EmailStr


class Feedback(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    message: Annotated[str, Field(min_length=10, max_length=500)]

    @field_validator("message", mode="before")
    def message_must_be_correct(cls, v):
        if contains_bad_words(v):
            raise ValueError("Использование недопустимых слов")
        return v
