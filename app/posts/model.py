from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, false, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(280), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    likes_count: Mapped[int] = mapped_column(Integer, server_default="0")
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=false())

    def __init__(self, content: str):
        self.content = content
