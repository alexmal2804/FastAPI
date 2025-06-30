from fastapi import FastAPI
import uvicorn
from fastapi.responses import FileResponse
import os
app = FastAPI()
@app.get("/")
def read_root():
    # Получаем абсолютный путь к файлу
    return {"message": "Hello World"}

@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!!!"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)