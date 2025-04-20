import logging
from fastapi import UploadFile

import fitz
from sqlmodel import Session

from models.resume import Resume
from models.user import User
from repositories.resume import ResumeRepository


logger = logging.getLogger()


class ResumeOrchestrator:
    def __init__(self, user: User, session: Session):
        self.user = user
        logger.info(self.user)
        self.session = session

        self.repo = ResumeRepository(session)

    async def upload_resume(self, name: str, file: UploadFile) -> Resume:
        """Upload a resume for this user"""
        content = await self._parse_resume(file)

        # TODO: lots of processing (vectorization?)
        resume = Resume(user_id=self.user.id, name=name, content=content)
        return self.repo.create(resume)

    async def _parse_resume(self, file: UploadFile) -> str:
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        extracted_text = "\n".join(page.get_text() for page in doc)

        return extracted_text
