from fastapi import FastAPI, File, UploadFile, Depends, status
import datetime
from typing import List
from pathlib import Path
from fastapi.responses import JSONResponse, FileResponse
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import PostBase

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/post", status_code=status.HTTP_200_OK)
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"data": post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}












# create directory
BASE_UPLOAD_DIR = Path("files/")
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/file/{directory}/", status_code=status.HTTP_201_CREATED)
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

