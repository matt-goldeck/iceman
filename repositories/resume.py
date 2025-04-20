from sqlmodel import Session

from models.resume import Resume
from repositories.base import BaseRepository


class ResumeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Resume, session)
