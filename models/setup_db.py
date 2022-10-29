from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Transaction
from models.meta import Base

def setup_db(engine):
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    first_transaction = Transaction(symbol="ETH", name="Ethereum", current_price=101.1545451)
    session.add(first_transaction)
    session.commit()

    return session