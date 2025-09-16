from sqlmodel import Field, SQLModel
from datetime import datetime


class Note(SQLModel):
    __tablename__ = "notes"
    __route__ = "notes"

    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True, nullable=False)
    content: str = Field(nullable=False)
    timestamp: datetime | None = Field(default_factory=datetime.now, index=True)
