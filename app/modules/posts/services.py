from sqlalchemy.orm import Session
from app.modules.posts import schemas, models


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_posts_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()
