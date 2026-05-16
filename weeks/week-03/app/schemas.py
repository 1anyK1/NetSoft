from pydantic import BaseModel
from typing import Optional

class CommentBase(BaseModel):
    text: str
    author: str
    rating: Optional[int] = None
    post_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    
    class Config:
        from_attributes = True