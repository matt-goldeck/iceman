import logging
from fastapi import UploadFile

import fitz
from sqlmodel import Session

from models.resume import Resume
from models.user import User
from repositories.resume import ResumeRepository
from utils.storage import get_or_create_bucket_for_user, upload_file_to_bucket


logger = logging.getLogger()


class ResumeService:
    def __init__(self, user: User, session: Session):
        self.user = user
        self.session = session

        self.repo = ResumeRepository(session)
        self.bucket = get_or_create_bucket_for_user(user.id)

    async def upload_resume(self, name: str, file: UploadFile) -> Resume:
        """Upload a resume for this user"""
        self.validate_resume(file)

        file_bytes = await file.read()

        # Parse raw content and write to DB
        content = self._parse_resume_from_bytes(file_bytes)
        resume = self.repo.create(
            Resume(user_id=self.user.id, name=name, content=content)
        )

        # Store PDF in Supabase storage
        filename = f"resumes/{resume.id}.pdf"
        upload_file_to_bucket(
            file=file_bytes,
            bucket_name=self.bucket.name,
            file_name=filename,
        )

        return resume

    def validate_resume(self, file: UploadFile) -> None:
        """Validate a resume for this user"""
        # TODO: this should be WAY more robust and secure
        if not file.filename.endswith((".pdf")):
            raise ValueError("File must be a PDF")

    def _parse_resume_from_bytes(self, file_bytes: bytes) -> str:
        """Extract plaintext from a PDF file"""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        extracted_text = "\n".join(page.get_text() for page in doc)

        return extracted_text
