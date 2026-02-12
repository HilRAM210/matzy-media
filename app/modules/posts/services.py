from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload
from app.modules.posts import schemas, models


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Post)
        .options(joinedload(models.Post.user), joinedload(models.Post.votes))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_posts_by_id(db: Session, post_id: int):
    return (
        db.query(models.Post)
        .options(joinedload(models.Post.user), joinedload(models.Post.votes))
        .filter(models.Post.id == post_id)
        .first()
    )


def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = get_posts_by_id(db, post_id)
    if not db_post:
        return None

    update_data = post_update.dict(exclude_unset=True)

    if not update_data:
        return db_post

    stmt = (
        update(models.Post)
        .where(models.Post.id == post_id)
        .values(**update_data)
        .returning(models.Post)
    )
    result = db.execute(stmt)
    db.commit()
    updated_post = result.scalar_one()
    db.refresh(updated_post)
    return updated_post


def delete_post(db: Session, post_id: int):
    db_post = get_posts_by_id(db, post_id)
    if not db_post:
        return None

    db.delete(db_post)
    db.commit()
    return True
