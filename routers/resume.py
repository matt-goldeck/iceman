import logging
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session

from models.user import User
from services.resume import ResumeService
from utils.auth import get_current_user
from utils.db import get_session


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/upload/")
async def upload_resume(
    name: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Upload a resume for this user"""
    service = ResumeService(user, session)
    await service.upload_resume(name, file)

    return {"status": "success"}
