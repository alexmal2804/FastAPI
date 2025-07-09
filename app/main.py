from email.header import Header
from math import dist
from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated, Optional

from fastapi.security import HTTPBearer
from .db import fake_users_db
from .models import User, UserInDB
from .security import (
    create_jwt_token,
    get_user_from_token,
)

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

auth_scheme = HTTPBearer() # Define the auth scheme for dependency injection

@app.post("/login")
async def login(user: User):
    logging.info(f"Received login request for user: {user.username}")
    # Check if the user exists in the fake database
    for db_user in fake_users_db:
        logging.info(f"Checking user: {db_user['username']}")
        if (
            db_user["username"] == user.username
            and user.password == db_user["password"]
        ):
            # Create a UserInDB instance
            user_in_db = UserInDB(
                username=db_user["username"], password=db_user["password"]
            )
            # Create a JWT token for the user
            token = create_jwt_token(user_in_db)
            logging.info(f"Token generated: {token}")
            return {"access_token": token, "token_type": "bearer"}
    # If user not found, raise an HTTP exception
    raise HTTPException(status_code=400, detail="Invalid username or password")


@app.get("/protected_secure", dependencies=[Depends(auth_scheme)])
async def protected_secure(user: UserInDB = Depends(get_user_from_token)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "This is a protected route", "user": user}
