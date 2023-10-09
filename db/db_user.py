from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db.models import DbUser
from hashing import Hash
from schemas.schemas import UserBase


def create_user(request: UserBase, db: Session):
    """Create new User in DB"""
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    """Get all Users from DB"""
    return db.query(DbUser).all()


def get_user(id: int, db: Session):
    """Get User by ID from DB"""
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user


def update_user(request: UserBase, db: Session, id: int):
    """Update User in DB"""
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return "user updated"


def delete_user(db: Session, id: int):
    """Delete User from DB"""
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    db.delete(user)
    db.commit()
    return "user deleted"


def get_user_by_username(db: Session, username: str):
    """Get user by ID from DB"""
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with name: {username} not found")
    return user

