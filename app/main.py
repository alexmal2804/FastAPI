from typing import Annotated
from fastapi import FastAPI, HTTPException, Header, Request
import re
import datetime
from .models import CommonHeaders

app = FastAPI()

reg_accept_language = re.compile(
    r"^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*"
    r"(\s*;\s*q=(0(\.[0-9]{1,3})?|1(\.0{1,3})?))?"
    r"(\s*,\s*[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*"
    r"(\s*;\s*q=(0(\.[0-9]{1,3})?|1(\.0{1,3})?))?)*$"
)

MINIMUM_APP_VERSION = "0.0.2"

@app.get("/headers")
def get_headers(headers: Annotated[CommonHeaders, Header()]):
    if headers.user_agent is None:
        raise HTTPException(status_code=400, detail="User-Agent header is required")
    if headers.accept_language is None:
        raise HTTPException(
            status_code=400, detail="Accept-Language header is required"
        )
    x_current_version = headers.x_current_version
    if x_current_version is None:
        raise HTTPException(status_code=400, detail="X-Current-Version header is required")
    if x_current_version < MINIMUM_APP_VERSION:
        raise HTTPException(
            status_code=422,
            detail=f"X-Current-Version must be at least {MINIMUM_APP_VERSION}"
        )
    return {"headers": headers}


@app.get("/info")
def get_info(headers: Annotated[CommonHeaders, Header()]):
    if headers.user_agent is None:
        raise HTTPException(status_code=400, detail="User-Agent header is required")
    if headers.accept_language is None:
        raise HTTPException(
            status_code=400, detail="Accept-Language header is required"
        )
    x_server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x_current_version = headers.x_current_version
    if x_current_version is None:
        raise HTTPException(status_code=400, detail="X-Current-Version header is required")
    if x_current_version < MINIMUM_APP_VERSION:
        raise HTTPException(
            status_code=422,
            detail=f"X-Current-Version must be at least {MINIMUM_APP_VERSION}"
        )
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": headers,
        "X-Server-Time": x_server_time
    }
