from sqlmodel import Session

from models.job_listing import CompatibilityScore, JobListing
from repositories.base import BaseRepository


class JobListingRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(JobListing, session)


class CompatibilityScoreRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(CompatibilityScore, session)
