from uuid import UUID

from pydantic import BaseModel


class DislikesResponse(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
