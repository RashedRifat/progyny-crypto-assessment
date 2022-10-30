"""Crypto Interview Assessment Module."""

import os, requests, json
from turtle import position 
import crypto_api as ca
from sqlalchemy import create_engine
from models.setup_db import setup_db
from models.models import Transaction, Portfolio_Item
from core.logic import get_data, update_cost_basis, display_position_balance
from dotenv import find_dotenv, load_dotenv

def run():
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

        # if a coin was purchased, update our portfolio 
        if entry["purchased"] or entry["symbol"] == "usdt":
            bid = ca.submit_order(entry["coin_id"], 1, entry["current_price"])
            position = session.query(Portfolio_Item).filter_by(symbol=Transaction.symbol).first()
            
            # add a new position if ti does not exist 
            if position == None:
                position = Portfolio_Item(
                    coin_id=entry["coin_id"], name=entry["name"], symbol=entry["symbol"], 
                    cost_basis=bid, coins_held=1)
                session.add(position)

            # else update the current value 
            else:
                position.cost_basis = update_cost_basis(position, bid)
                position.coins_held += 1 

    # Commit all pending transactions to the database         
    session.commit()
    
    # Display current portfolio 
    for position in session.query(Portfolio_Item).order_by(Portfolio_Item.coin_id):
        print(display_position_balance(position, ca.get_current_price(position.coin_id)))

if __name__ == "__main__":
    run()