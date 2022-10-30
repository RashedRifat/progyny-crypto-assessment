"""Crypto Interview Assessment Module."""

import os, requests, json 
import crypto_api as ca
from sqlalchemy import create_engine
from models.setup_db import setup_db
from models.models import Transaction, Portfolio_Item
from core.logic import get_data
from dotenv import find_dotenv, load_dotenv

if __name__ == "__main__":
    load_dotenv(find_dotenv(raise_error_if_not_found=True))

    # Create engine and setup the database 
    engine = create_engine(f"sqlite:///{os.getenv('DB_HOST')}", echo=True)
    session = setup_db(engine)
    data = get_data()

    # for each of the top coins, add the record to the database 
    for entry in data.values():
        entry["purchased"] = 1 if entry["current_price"] < entry["historical_average"] else 0
        record = Transaction(**entry)
        session.add(record)

        # TODO: update portfolio datavase 
        # if a coin was purchased, update our portfolio 

    session.commit()
    
    # TODO: display current portfolio 
