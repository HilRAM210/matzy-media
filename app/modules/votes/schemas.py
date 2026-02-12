from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

from app.modules.posts import schemas


class VoteType(int, Enum):
    UPVOTE = 1
    DOWNVOTE = -1


class VoteCreate(BaseModel):
    post_id: int
    vote_type: Literal[1, -1]


class VoteUpdate(BaseModel):
    vote_type: Literal[1, -1]


class VoteOut(BaseModel):
    user_id: int
    post_id: int
    vote_type: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostWithVoteStatus(BaseModel):
    post_id: int
    vote_score: int
    user_vote: Optional[int] = None


class PostWithVotes(schemas.PostOut):
    vote_score: int = 0
    user_vote: Optional[int] = None
