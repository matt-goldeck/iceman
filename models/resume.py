from datetime import datetime
import uuid
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    model_config = ConfigDict(extra="ignore")

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID

    name: str
    content: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
