from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Transaction
from models.meta import Base

def setup_db(engine : "SQLAlchemy.Engine") -> "SQLAlchemy.Session":
    """Setup for the SQLite Database

    Args:
        engine (SQLAlchemy.Engine): the engine for SQLAlchemy

    Returns:
        session: a session bound to the SQLAlchemy engine
    """

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session