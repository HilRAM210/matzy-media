from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from typing import Optional, List

from app.modules.users.schemas import UserOut


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class PostOut(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostWithUser(PostOut):
    user: UserOut


class VoteInfo(BaseModel):
    user_id: int
    vote_type: int

    class Config:
        from_attributes = True


class VoteSummary(BaseModel):
    upvotes: int = 0
    downvotes: int = 0


class PostWithDetails(PostOut):
    user: UserOut
    votes: VoteSummary

    class Config:
        from_attributes = True
