from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from schemas.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    """Create User endpoint"""
    return db_user.create_user(request, db)


@router.get("/", response_model=List[UserDisplay])
def get_users(db: Session = Depends(get_db)):
    """Get Users endpoint"""
    return db_user.get_users(db)


@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    """Get User by ID endpoint"""
    return db_user.get_user(id, db)


@router.put("/{id}")
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    """Update User endpoint"""
    return db_user.update_user(request, db, id)


@router.delete("/{id}")
def update_user(id: int, db: Session = Depends(get_db)):
    """Delete User endpoint"""
    return db_user.delete_user(db, id)

