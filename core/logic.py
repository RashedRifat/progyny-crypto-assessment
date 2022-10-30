from typing import Dict
import crypto_api as ca
from models.models import Portfolio_Item

def get_historical_avg(coin_id : str) -> float:
    """Returns the historical average of a coin, over 10 days 

    Args:
        coin_id (str): the coin to get the historical average for

    Returns:
        float: the historical average
    """

    prices = ca.get_coin_price_history(coin_id)
    avg_price = sum([p[-1] for p in prices]) / len(prices) * 1.0
    return round(avg_price, 6)

def get_data() -> Dict:
    """Get data for the current top 3 coins

    Returns:
        Dict: data on the top 3 coins, including name, symbol, current price 
                historical average 
    """ 
    top_coins = ca.get_coins()[:3]
    data = {
        coin["id"] : {
            "coin_id" : coin["id"], 
            "symbol" : coin["symbol"], 
            "name" : coin["name"], 
            "current_price" : coin["current_price"], 
            "historical_average" : get_historical_avg(coin["id"])
        } for coin in top_coins
    } 
    return data


def update_cost_basis(position : Portfolio_Item, bid : float) -> float:
    prev_basis = position.cost_basis * position.coins_held
    new_basis = (prev_basis + bid) / (position.coins_held + 1)
    return new_basis

def display_position_balance(position : Portfolio_Item, current_price : float) -> str:
    pct_change = (current_price - position.cost_basis) / position.cost_basis
    pct_change = round(pct_change * 100, 2)

    return 'Name: {} Symbol: {} Coins_Held: {} Percent_Change: {:.2f}%'.format(
        position.name, position.symbol, position.coin_id, pct_change
    )