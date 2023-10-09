import datetime

from sqlalchemy.orm import Session

from db.models import DbComment
from schemas.schemas import CommentBase


def create_comment(request: CommentBase, db: Session):
    """Create new Comment in DB"""
    new_comment = DbComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.datetime.now(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all_comments(db: Session, post_id: int):
    """Get all Comments by post_id from DB"""
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()
