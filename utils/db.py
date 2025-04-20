from contextlib import contextmanager
from functools import wraps

from sqlalchemy import NullPool
from sqlmodel import Session, create_engine

from settings import settings


def get_engine():
    db_name = f"postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    return create_engine(db_name)


engine = get_engine()


def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def session_context():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(func):
    """Wrap a class method with a session context manager."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        with session_context() as session:
            return func(self, session, *args[1:], **kwargs)

    return wrapper
