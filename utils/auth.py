import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from sqlmodel import Session

from models.user import User
from repositories.exceptions import ObjectNotFoundException
from repositories.user import UserRepository
from utils.db import get_session
from utils.supabase import get_supabase_client

logger = logging.getLogger()


async def get_current_user(
    token: Annotated[str, Depends(HTTPBearer())],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """Dependency for getting the current user from a request's token."""
    supabase = get_supabase_client()

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
