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


def update_cost_basis(position : Portfolio_Item, bid : float, quantity : int = 1) -> float:
    """Returns the updated cost basis for a position

    Args:
        position (Portfolio_Item): the portfolio item representing the position
        bid (float): the current bid
        quantity (int, optional): quantity of coins to purchase. Defaults to 1.

    Returns:
        float: the updated cost basis. The position item is left unchanged
    """

    prev_basis = position.cost_basis * position.coins_held
    new_basis = (prev_basis + bid) / (position.coins_held + quantity)
    return new_basis

def display_position_balance(position : Portfolio_Item, current_price : float) -> str:
    """Displays the current status of a position

    Args:
        position (Portfolio_Item): the position to display the balance for
        current_price (float): the current price of the position asset

    Returns:
        str: a description of the position, including name, symbol, coins held
            and percent change (gain or loss) of the position. 
    """

    pct_change = (current_price - position.cost_basis) / position.cost_basis
    pct_change = round(pct_change * 100, 2)

    return f"PORTFOLIO_POSITION - Name: {position.name}, Symbol: {position.symbol}, " + \
        f"Coins_Held: {position.coins_held} Percent_Change: {pct_change:.2f}%"