from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db import db_comment
from db.database import get_db
from schemas.schemas import CommentBase, UserAuth

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.get("/all/{post_id}")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Get all Comments by post_id endpoint"""
    return db_comment.get_all_comments(db, post_id)


@router.post("/")
def create_comment(
        request: CommentBase,
        db: Session = Depends(get_db),
        current_user: UserAuth = Depends(get_current_user)
):
    """Create Comment endpoint"""
    return db_comment.create_comment(request, db)
