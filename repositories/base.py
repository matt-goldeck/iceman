import logging
from sqlalchemy import select
from sqlmodel import SQLModel, Session
from sqlalchemy.orm import exc as sqlalchemy_orm_err
from sqlalchemy import exc as sqlalchemy_exc

from repositories.exceptions import ObjectNotFoundException, UnicityViolationException


logger = logging.getLogger()


class BaseRepository:
    """Base class abstracting interaction with a database table."""

    def __init__(self, model_class: SQLModel, session: Session):
        self.model_class = model_class
        self.session = session

    def get(self, value, field="id") -> SQLModel:
        """Retrieve a single item from this table"""
        statement = select(self.model_class).where(
            getattr(self.model_class, field) == value
        )
        results = self.session.exec(statement)
        try:
            return results.one_or_none()[0]
        except sqlalchemy_orm_err.NoResultFound:
            raise ObjectNotFoundException()

    def create(self, obj: SQLModel) -> SQLModel:
        """Create a new item in this table"""
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except sqlalchemy_exc.IntegrityError as e:
            raise UnicityViolationException()

    def refresh(self, obj: SQLModel) -> SQLModel:
        """Refresh an object from the database"""
        self.session.refresh(obj)
        return obj
