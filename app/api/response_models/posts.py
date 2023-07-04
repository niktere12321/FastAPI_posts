from uuid import UUID

from pydantic import BaseModel
from .likes import LikesResponse
from .dislikes import DislikesResponse


class PostsResponse(BaseModel):
    id: UUID
    title: str
    description: str
    user_id: UUID
    likes: list[LikesResponse]
    dislikes: list[DislikesResponse]

    class Config:
        orm_mode = True
