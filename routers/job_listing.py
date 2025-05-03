import logging
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from llms.openai import OpenAIAgent
from models.job_listing import CompatibilityScore, JobListing
from models.resume import Resume
from models.user import User
from repositories.exceptions import ObjectNotFoundException
from repositories.job_listing import CompatibilityScoreRepository, JobListingRepository
from repositories.resume import ResumeRepository
from services.compatibility_scoring import CompatibilityScoringService
from services.constants import OpenAIModel
from utils.auth import get_current_user
from utils.db import get_session


router = APIRouter()

logger = logging.getLogger(__name__)

# == Routes ==


@router.post("/{job_listing_id}/compatibility/{resume_id}/")
async def create_compatibility_score(
    job_listing_id: uuid.UUID,
    resume_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> CompatibilityScore:
    """
    Calculate a compatibility score between a job listing and a resume.
    """
    job_listing = _get_job_listing_for_user(job_listing_id, user, session)
    resume = _get_resume_for_user(resume_id, user, session)

    existing_score = _get_existing_score(job_listing.id, resume.id, session)
    if existing_score:
        raise HTTPException(
            409,
            "A compatibility score already exists for this job listing and resume.",
        )

    service = CompatibilityScoringService(
        llm=OpenAIAgent(OpenAIModel.gpt_4_1_mini),
        session=session,
    )
    score = service.score(job_listing=job_listing, resume=resume)

    return score


# == Helpers ==


def _get_job_listing_for_user(
    job_listing_id: uuid.UUID,
    user: User,
    session: Session,
) -> JobListing:
    """Get a job listing for a user"""
    try:
        return JobListingRepository(session).multi_field_get(
            {"id": job_listing_id, "user_id": user.id}
        )
    except ObjectNotFoundException:
        raise HTTPException(404, "A job listing with this ID does not exist.")


def _get_resume_for_user(
    resume_id: uuid.UUID,
    user: User,
    session: Session,
) -> Resume:
    """Get a resume for a user"""
    try:
        return ResumeRepository(session).multi_field_get(
            {"id": resume_id, "user_id": user.id}
        )
    except ObjectNotFoundException:
        raise HTTPException(404, "A resume with this ID does not exist.")


def _get_existing_score(
    job_listing_id: uuid.UUID,
    resume_id: uuid.UUID,
    session: Session,
) -> Optional[CompatibilityScore]:
    """Get an existing compatibility score"""
    try:
        return CompatibilityScoreRepository(session).multi_field_get(
            {"job_listing_id": job_listing_id, "resume_id": resume_id}
        )
    except ObjectNotFoundException:
        return None
