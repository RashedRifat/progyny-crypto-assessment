from typing import Dict
import crypto_api as ca

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
            "name" : coin["name"], 
            "symbol" : coin["symbol"], 
            "current_price" : coin["current_price"], 
            "historical_average" : get_historical_avg(coin["id"])
        } for coin in top_coins
    } 
    return data