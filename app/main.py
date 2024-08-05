from fastapi import FastAPI, File, UploadFile, Depends
import datetime
from typing import List
from pathlib import Path
from fastapi.responses import JSONResponse, FileResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

while True:
    try:
        connect = psycopg2.connect(
            host="localhost",
            database="FastAPI",
            user="postgres",
            password="P@rajuli17",
            cursor_factory=RealDictCursor
        )
        cursor = connect.cursor()
        print("Database connection success")
        break
    except Exception as e:
        print("Error:", e)

# @app.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user(db: Session = Depends(get_db)):


# create directory
BASE_UPLOAD_DIR = Path("files/")
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/file/{directory}/")
async def upload_file(directory: str, files: List[UploadFile] = File(...)):
    sub_dir = BASE_UPLOAD_DIR / directory
    sub_dir.mkdir(parents=True, exist_ok=True)
    urls = []
    for file in files:
        datetimenow = str(datetime.datetime.now()).replace(" ", ".")
        file_name = f"{datetimenow}-{file.filename}"
        file_path = sub_dir / file_name
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_url = f"http://localhost:8000/file/{directory}/{file_name}/"
        urls.append(file_url)
    return JSONResponse(content={"url": urls})


@app.get("/file/{directory}/{filename}/")
async def get_file(directory: str, filename: str):
    file_path = BASE_UPLOAD_DIR / directory / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)


@app.get("/file/{directory}/")
async def get_file_list(directory: str):
    sub_dir = BASE_UPLOAD_DIR / directory
    if sub_dir.exists() and sub_dir.is_dir():
        print(sub_dir.iterdir())
        files = [f"http://localhost:8000/file/{directory}/{file.name}" for file in sub_dir.iterdir() if file.is_file()]
        return JSONResponse(content={"files": files})
    return JSONResponse(content={"error": "File not found"}, status_code=404)

