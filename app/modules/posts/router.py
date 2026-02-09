from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.posts import models, schemas, services, dependencies
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


# Ambil semua postingan
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db)):
    posts = services.get_posts(db)
    return posts


# Buat postingan baru
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = services.create_post(db=db, post=post, user_id=current_user.id)
    return new_post


# Ambil satu postingan berdasarkan id
@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_one_post(post_id: int, db: Session = Depends(get_db)):
    post = services.get_posts_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} was not found",
        )
    return post


# Hapus Postingan
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} was not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authotized to perform request actions",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update postingan
@router.put("/{post_id}", response_model=schemas.PostOut)
async def delete_post(
    post_id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} was not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authotized to perform request actions",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
