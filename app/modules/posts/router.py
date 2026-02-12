from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from app.modules.posts import models, schemas, services, dependencies
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


# Ambil semua postingan
@router.get("/", response_model=List[schemas.PostWithDetails])
async def get_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(get_current_user),
):
    posts = services.get_posts(db, skip=skip, limit=limit)
    result = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "user": post.user,
            "votes": {
                "upvotes": sum(1 for v in post.votes if v.vote_type == 1),
                "downvotes": sum(1 for v in post.votes if v.vote_type == -1),
            },
        }
        result.append(post_dict)

    return result


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
@router.get("/{post_id}", response_model=schemas.PostWithDetails)
async def get_one_post(
    post: models.Post = Depends(dependencies.get_post_by_id),
    current_user: int = Depends(get_current_user),
):
    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "user": post.user,
        "votes": {
            "upvotes": sum(1 for v in post.votes if v.vote_type == 1),
            "downvotes": sum(1 for v in post.votes if v.vote_type == -1),
        },
    }
    return post_dict


# Hapus Postingan
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: models.Post = Depends(dependencies.get_post_for_owner),
    db: Session = Depends(get_db),
):
    services.delete_post(db, post.id)
    return None


# Update postingan
@router.put("/{post_id}", response_model=schemas.PostOut)
async def delete_post(
    post_update: schemas.PostUpdate,
    post: models.Post = Depends(dependencies.get_post_for_owner),
    db: Session = Depends(get_db),
):
    updated_post = services.update_post(db=db, post_id=post.id, post_update=post_update)
    return updated_post
