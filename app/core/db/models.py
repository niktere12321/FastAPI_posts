import re
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import validates, relationship
from sqlalchemy.schema import ForeignKey
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


@as_declarative()
class Base:
    """Базовая модель."""
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    __name__: str


class User(SQLAlchemyBaseUserTable[uuid.uuid4], Base):
    """Модель для пользователей."""
    __tablename__ = "users"

    name = Column(String(length=100), nullable=False)
    surname = Column(String(length=100), nullable=False)
    email = Column(String(length=150), nullable=False, unique=True)

    def __repr__(self):
        return f'<User: {self.id}, name: {self.name}, surname: {self.surname}>'


class Posts(Base):
    """Посты."""
    __tablename__ = "posts"

    title = Column(String(length=50), nullable=False)
    description = Column(String(length=150), nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False
    )
    likes = relationship("Likes", cascade='delete', lazy="selectin")
    dislikes = relationship("Dislikes", cascade='delete', lazy="selectin")

    def __repr__(self):
        return f"<Posts: {self.id}, title: {self.title}>"


class Likes(Base):
    """Лайки."""
    __tablename__ = "likes"

    post_id = Column(
        UUID(as_uuid=True), ForeignKey(Posts.id, ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self):
        return f'<Likes: {self.id}, post_id: {self.post_id}, user_id: {self.user_id}>'


class Dislikes(Base):
    """Дизлайки."""
    __tablename__ = "dislikes"

    post_id = Column(
        UUID(as_uuid=True), ForeignKey(Posts.id, ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self):
        return f'<Dislikes: {self.id}, post_id: {self.post_id}, user_id: {self.user_id}>'
