from pydantic import BaseModel, Extra


class PostsCreateAndUpdateRequest(BaseModel):
    title: str
    description: str

    class Config:
        extra = Extra.forbid
