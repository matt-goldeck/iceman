from typing import Optional
import uuid

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    model_config = ConfigDict(extra="ignore")

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str

    first_name: Optional[str] = None
    last_name: Optional[str] = None
