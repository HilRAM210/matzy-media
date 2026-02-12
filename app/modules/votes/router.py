from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.votes import schemas, services
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/votes", tags=["Votes"])


# Buat atau update vote
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteOut)
async def vote(
    vote: schemas.VoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Verifikasi post exists
    from app.modules.posts import services as post_services

    post = post_services.get_posts_by_id(db, vote.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist",
        )

    new_vote = services.create_or_update_vote(db=db, vote=vote, user_id=current_user.id)
    return new_vote


# Hapus vote
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    vote = services.get_vote(db, post_id=post_id, user_id=current_user.id)

    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found",
        )

    services.delete_vote(db, post_id=post_id, user_id=current_user.id)
    return None
