from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.posts.dependencies import get_post_by_id
from app.modules.votes import services


def validate_post_for_vote(
    post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    post = get_post_by_id(post_id, db)

    if post.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot vote on your own post",
        )

    return post


def get_vote_or_404(
    post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    vote = services.get_user_vote(db, current_user.id, post_id)

    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )

    return vote
