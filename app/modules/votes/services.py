from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.modules.votes import models, schemas
from app.modules.posts import models as post_models


def create_or_update_vote(db: Session, user_id: int, post_id: int, vote_type: int):
    existing_vote = get_user_vote(db, user_id, post_id)

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return delete_vote(db, user_id, post_id)
        else:
            existing_vote.vote_type = vote_type
            db.commit()
            db.refresh(existing_vote)
            return existing_vote
    else:
        db_vote = models.Vote(user_id=user_id, post_id=post_id, vote_type=vote_type)
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote


def delete_vote(db: Session, user_id: int, post_id: int):
    vote = get_user_vote(db, user_id, post_id)
    if vote:
        db.delete(vote)
        db.commit()
        return True
    return False


def get_user_vote(db: Session, user_id: int, post_id: int):
    return (
        db.query(models.Vote)
        .filter(and_(models.Vote.user_id == user_id, models.Vote.post_id == post_id))
        .first()
    )


def get_post_vote_score(db: Session, post_id: int):
    result = (
        db.query(func.coalesce(func.sum(models.Vote.vote_type), 0))
        .filter(models.Vote.post_id == post_id)
        .scalar()
    )

    return result or 0


def get_posts_with_user_votes(db: Session, user_id: int, post_ids: list[int]):
    votes = (
        db.query(models.Vote)
        .filter(and_(models.Vote.user_id == user_id, models.Vote.post_id.in_(post_ids)))
        .all()
    )

    return {vote.post_id: vote.vote_type for vote in votes}
