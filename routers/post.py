import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db import db_post
from db.database import get_db
from schemas.schemas import PostDisplay, PostBase, UserAuth
import string
import random

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ["absolute", "relative"]


@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    """Upload Image endpoint"""
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(6))
    new = f"_{random_string}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}


@router.post("", response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """Create Post endpoint"""
    if request.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type can only take values 'absolute', 'relative'"
        )
    return db_post.create_post(request, db)


@router.get("/all", response_model=List[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    """Get all Post endpoint"""
    return db_post.get_all_posts(db)


@router.get("/{id}", response_model=PostDisplay)
def get_post(id: int, db: Session = Depends(get_db)):
    """Get Post by ID endpoint"""
    return db_post.get_post_by_id(id, db)


@router.delete('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    """Delete Post endpoint"""
    return db_post.delete_post(db, id, current_user.id)
