from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel):
    __tablename__ = "users"
    __route__ = "users"

    id: int | None = Field(default=None, primary_key=True, index=True)
    nickname: str = Field(index=True, nullable=False)
    name: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    timestamp: datetime | None = Field(default_factory=datetime.now, index=True)
