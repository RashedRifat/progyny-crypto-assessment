import unittest, sys 
from unittest.mock import MagicMock, patch

sys.path.append("..")
from core.logic import * 
from models.models import Portfolio_Item

class Test_Core_Logic(unittest.TestCase):

    def setUp(self) -> None:
        self.portfolio_item = Portfolio_Item(
            coin_id="ForestCoin", symbol="FC", name="ForestCoin", 
            cost_basis=10, coins_held=4
        )

    def test_update_cost_basis_increase(self):
        actual = update_cost_basis(self.portfolio_item, 15)
        self.assertEqual(actual, 11)

    def test_update_cost_basis_decrease(self):
        actual = update_cost_basis(self.portfolio_item, 5)
        self.assertEqual(actual, 9)

    def test_update_cost_basis_no_change(self):
        actual = update_cost_basis(self.portfolio_item, 10)
        self.assertEqual(actual, 10)

    def test_display_position_balance_no_change(self):
        expected = 'PORTFOLIO_POSITION - Name: ForestCoin, Symbol: FC, Coins_Held: 4 Percent_Change: 50.00%'
        actual = display_position_balance(self.portfolio_item, 15)
        self.assertEqual(expected, actual)

    def test_display_position_balance_increase(self):
        expected = 'PORTFOLIO_POSITION - Name: ForestCoin, Symbol: FC, Coins_Held: 4 Percent_Change: 0.00%'
        actual = display_position_balance(self.portfolio_item, 10)
        self.assertEqual(expected, actual)

    def test_display_position_balance_decrease(self):
        expected = 'PORTFOLIO_POSITION - Name: ForestCoin, Symbol: FC, Coins_Held: 4 Percent_Change: -50.00%'
        actual = display_position_balance(self.portfolio_item, 5)
        self.assertEqual(expected, actual)

    @patch("crypto_api.requests")
    def test_get_historical_avg(self, mock_requests):

        # create mocked api response 
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "prices" : [(0, 10), (0, 10), (0, 10)]
        }

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_historical_avg("demo"), 10)


if __name__ == "__main__":    
    unittest.main(verbosity=2)