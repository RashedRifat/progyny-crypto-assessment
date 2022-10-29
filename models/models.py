from sqlalchemy import Column, Integer, String, DateTime, Sequence, Numeric
from datetime import datetime
from models.meta import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, Sequence("transaction_id_seq") ,primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    symbol = Column(String)
    name = Column(String)
    current_price = Column(Numeric(10,5))

    def __str__(self) -> str:
        return 'ID: {} Timestamp: {} Symbol: {} Name: {} Current_Price: {}'.format(
            self.id, self.timestamp, self.symbol, self.name, self.current_price 
        )

    def __repr__(self) -> str:
        return self.__str__()

class Portfolio_Item(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, Sequence("portfolio_id_seq") ,primary_key=True)
    symbol = Column(String)
    cost_basis = Column(Numeric(10,2))
    coins_held = Column(Integer)

    def __str__(self) -> str:
        return 'ID: {} Symbol: {} Cost_Basis: {} Coins_Held: {}'.format(
            self.id, self.symbol, self.cost_basis, self.coins_held
        )

    def __repr__(self) -> str:
        return self.__str__()