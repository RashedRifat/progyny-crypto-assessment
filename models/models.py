from sqlalchemy import Column, Integer, String, DateTime, Sequence, Numeric
from sqlalchemy.dialects.sqlite import DECIMAL
from datetime import datetime
from models.meta import Base

class Transaction(Base):
    """ Model to represent a transaction (or record) of cryptocurrencies.  
    """

    __tablename__ = "transactions"
    id = Column(Integer, Sequence("transaction_id_seq") ,primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    coin_id = Column(String)
    symbol = Column(String)
    name = Column(String)
    current_price = Column(DECIMAL(10,7))
    historical_average = Column(DECIMAL(10,7))
    purchased = Column(Integer)  # storing trade data in the same table to avoid data redundancy 

    def __str__(self) -> str:
        return 'ID: {} Timestamp: {} Coin_ID: {} Symbol: {} Name: {} Current_Price: {} Historical Average: {} Purchased: {}'.format(
            self.id, self.timestamp, self.coin_id, self.symbol, self.name, self.current_price, self.historical_average, self.purchased
        )

    def __repr__(self) -> str:
        return self.__str__()

class Portfolio_Item(Base):
    """Model to represent a position of a cryptocurrency portfolio. 
    """

    __tablename__ = "portfolio"
    coin_id = Column(String, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    cost_basis = Column(DECIMAL(10,7, asdecimal=False))
    coins_held = Column(Integer)

    def __str__(self) -> str:
        return 'Coin_ID: {} Symbol: {} Name: {} Cost_Basis: {} Coins_Held: {}'.format(
            self.coin_id, self.symbol, self.name, self.cost_basis, self.coins_held
        )

    def __repr__(self) -> str:
        return self.__str__()