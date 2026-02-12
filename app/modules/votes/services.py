from sqlalchemy.orm import Session
from app.modules.votes import schemas, models


def create_or_update_vote(db: Session, vote: schemas.VoteCreate, user_id: int):
    # Cek apakah vote sudah ada
    existing_vote = (
        db.query(models.Vote)
        .filter(models.Vote.user_id == user_id, models.Vote.post_id == vote.post_id)
        .first()
    )

    if existing_vote:
        # Update vote yang sudah ada
        existing_vote.vote_type = vote.vote_type
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    else:
        # Buat vote baru
        db_vote = models.Vote(**vote.dict(), user_id=user_id)
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote


def delete_vote(db: Session, post_id: int, user_id: int):
    vote = (
        db.query(models.Vote)
        .filter(models.Vote.user_id == user_id, models.Vote.post_id == post_id)
        .first()
    )

    if not vote:
        return None

    db.delete(vote)
    db.commit()
    return True


def get_vote(db: Session, post_id: int, user_id: int):
    return (
        db.query(models.Vote)
        .filter(models.Vote.user_id == user_id, models.Vote.post_id == post_id)
        .first()
    )
