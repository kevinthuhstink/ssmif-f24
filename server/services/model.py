""" The portfolio optimization model. """

from math import sqrt
from functools import reduce
import numpy as np
import pandas as pd
from pypfopt.risk_models import risk_matrix, fix_nonpositive_semidefinite
from pypfopt.efficient_frontier import EfficientFrontier
from .factors import m12_return_rate
from .price_fetching import fetch_prices

class TickerException(Exception):
    """ Has class variable self.ticker so you know which ticker doesn't work """
    def __init__(self, message, ticker):
        super().__init__(message)
        self.message = message
        self.ticker = ticker


class Model(EfficientFrontier):
    """ Carhart 4-factor model + Efficient Frontier

    :param model: Calculates annualized return rates for assets
    :typeof model: services.returns.Carhart4FactorModel
    :param tickers: Tickers to optimize a portfolio over
    :type tickers: str[]
    """
    def __init__(self, model, tickers):
        prices = fetch_prices(tickers)

        for ticker in prices:
            if prices[ticker].empty:
                raise TickerException(f"Ticker ${ticker.upper()} has no price data.", ticker)

        rates = {t: m12_return_rate(prices[t]) for t in prices}
        self.returns = pd.Series({t: model(r) for t, r in rates.items()})
        self.returns.name = "Expected Returns"
        self.risk_free_rate = model.risk_free_rates.iloc[-1]
        self.risk_matrix = fix_nonpositive_semidefinite(risk_matrix(prices))
        super().__init__(self.returns, self.risk_matrix)

    def __str__(self):
        returns = f"Returns:\n{self.returns}"
        risk = f"Var-Covar Matrix:\n{self.risk_matrix}"
        return f"{returns}\n\n{risk}"

    def portfolio_returns(self, weights):
        """ Predicts total portfolio return given portfolio weights

        :param weights: The weight of each asset in the portfolio
        :type weights: OrderedDict[str, float]

        :return: Annualized portfolio returns
        :rtype: float
        """
        return reduce(lambda acc, t: acc + weights[t] * self.returns[t], weights.keys(), 0)

    def portfolio_risk(self, weights):
        """ Determines total portfolio volatility given portfolio weights

        :param weights: The weight of each asset in the portfolio
        :type weights: OrderedDict[str, float]

        :return: Annualized portfolio risk
                 (one stddev of total value variation as fraction of total weight)
        :rtype: float
        """
        w = np.array(list(weights.values()))
        return sqrt((w[None, :] @ self.risk_matrix.to_numpy() @ w)[0])

    def sharpe_ratio(self, weights):
        """ Determines portfolio sharpe ratio given portfolio weights

        :param weights: The weight of each asset in the portfolio
        :type weights: OrderedDict[str, float]

        :return: sharpe ratio number
        :rtype: float
        """
        excess_returns = self.portfolio_returns(weights) - self.risk_free_rate
        return excess_returns / self.portfolio_risk(weights)
