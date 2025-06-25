from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def root():
    # Получаем абсолютный путь к файлу
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    print(f"Serving file from: {file_path}")  # Для отладки
    return FileResponse(file_path)