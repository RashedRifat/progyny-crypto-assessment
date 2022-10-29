"""Crypto Interview Assessment Module."""

import os, crypto_api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.setup_db import setup_db
from models.models import Transaction, Portfolio_Item
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))

# You can access the environment variables as such, and any variables from the .env file will be loaded in for you to use.
# os.getenv("DB_HOST")

if __name__ == "__main__":
    engine = create_engine("sqlite:///demo.db", echo=True)
    session = setup_db(engine)

    for instance in session.query(Transaction).order_by(Transaction.id.desc()):
        print(instance)