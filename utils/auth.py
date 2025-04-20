import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from sqlmodel import Session
from supabase import create_client, Client as SupabaseClient


from models.user import User
from repositories.exceptions import ObjectNotFoundException
from repositories.user import UserRepository
from settings import settings
from utils.db import get_session

# TODO: Migrate to SQLAlchemy
supabase: SupabaseClient = create_client(
    settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY
)

logger = logging.getLogger("uvicorn.error")


async def get_current_user(
    token: Annotated[str, Depends(HTTPBearer())],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """Dependency for getting the current user from a request's token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_resp = supabase.auth.get_user(token.credentials)
    except Exception as e:
        logger.error("Error getting user from Supabase: %s", e)
        raise credentials_exception

    if user_resp is None:
        logger.error("User response is None")
        raise credentials_exception

    try:
        user = UserRepository(session).get(user_resp.user.id)
    except ObjectNotFoundException as e:
        logger.error("User not found in database")
        raise credentials_exception from e

    return user
