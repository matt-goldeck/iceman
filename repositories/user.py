from sqlmodel import Session
from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)
