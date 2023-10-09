import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from db.models import DbPost, DbUser
from schemas.schemas import PostBase


def create_post(request: PostBase, db: Session):
    """Create new Post in DB"""
    user = db.query(DbUser).filter(DbUser.id == request.creator_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {request.creator_id} not found"
        )
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(db: Session):
    """Get all Posts from DB"""
    return db.query(DbPost).all()


def get_post_by_id(id: int, db: Session):
    """Get Post by ID from DB"""
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post


def delete_post(db: Session, id: int, user_id: int):
    """Delete Post from DB"""
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
              detail=f'Post with id {id} not found')
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
              detail='Only post creator can delete post')

    db.delete(post)
    db.commit()
    return 'post deleted'
