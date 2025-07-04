import inspect
import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing_extensions import Annotated, Optional


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


class User1(BaseModel):
    id: int
    username: str
    age: int
    email: EmailStr


class Contact(BaseModel):
    email: EmailStr
    phone: Annotated[str, Field(min_length=7, max_length=15, pattern=r"^[0-9]+$")] | None


class Feedback(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, description="Имя пользователя")]
    message: Annotated[Optional[str], Field(min_length=10, max_length=500)]
    contact: Annotated[Contact, Field(description="Контактная информация пользователя")]

    @field_validator("message", mode="before")
    def message_must_be_correct(cls, v):
        if contains_bad_words(v):
            raise ValueError("Использование недопустимых слов")
        return v


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    age: Annotated[int, Field(ge=0)] | None = None
    is_subscribed: Annotated[bool, Field(default=False)] | None = None
