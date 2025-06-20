from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
