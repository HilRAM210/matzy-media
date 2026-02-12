from pydantic import BaseModel, Field
from datetime import datetime


class VoteBase(BaseModel):
    post_id: int = Field(..., gt=0)
    vote_type: int = Field(..., ge=-1, le=1)


class VoteCreate(VoteBase):
    pass


class VoteOut(BaseModel):
    user_id: int
    post_id: int
    vote_type: int
    created_at: datetime

    class Config:
        from_attributes = True
