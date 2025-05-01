from datetime import datetime
from typing import Optional
import uuid
from pydantic import ConfigDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, SQLModel


class JobListing(SQLModel, table=True):
    __tablename__ = "job_listing"

    model_config = ConfigDict(extra="ignore")

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    user_id: uuid.UUID
    company_id: uuid.UUID
    resume_id: uuid.UUID

    title: str
    description: str
    user_notes: Optional[str] = None

    url = Optional[str] = None


class CompatibilityScore(SQLModel, table=True):
    __tablename__ = "compatibility_score"
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    job_listing_id: uuid.UUID
    resume_id: uuid.UUID

    total_score: int
    explanation: str
    score_breakdown: dict[str, Any] = Field(
        sa_column=Column(JSONB), description="Unstructured breakdown of the score"
    )
