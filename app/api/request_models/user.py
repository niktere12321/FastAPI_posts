from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    email: str


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    email: str
