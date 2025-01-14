""" The portfolio optimization model. """

from math import sqrt
from functools import reduce
from contextlib import closing
import numpy as np
import pandas as pd
from pypfopt.risk_models import risk_matrix, fix_nonpositive_semidefinite
from pypfopt.efficient_frontier import EfficientFrontier
from .sql import get_connection
from .factors import m12_return_rate
from .price_fetching import fetch_prices


class Model(EfficientFrontier):
    """ Carhart 4-factor model + Efficient Frontier

    :param model: Calculates annualized return rates for assets
    :typeof model: services.returns.Carhart4FactorModel
    :param tickers: Tickers to optimize a portfolio over
    :type tickers: str[]
    """
    def __init__(self, model, tickers):
        with closing(get_connection()) as con:
            self.prices = fetch_prices(con, tickers)

        rates = {t: m12_return_rate(self.prices[t]) for t in self.prices}
        self.curr_prices = self.prices.tail(1)
        self.returns = pd.Series({t: model(r) for t, r in rates.items()})
        self.returns.name = "Expected Returns"
        self.risk_free_rate = model.risk_free_rates.iloc[-1]
        self.risk_matrix = fix_nonpositive_semidefinite(risk_matrix(self.prices))
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
                        ORDER MATTERS! DO NOT CHANGE THE ORDER OF THE
                        ENTRIES FROM WHAT WAS ORIGINALLY CALCULATED AFTER
                        RUNNING THE PORTFOLIO OPTIMIZER
        :type weights: OrderedDict[str, float]

        :return: Annualized portfolio risk
                 (one stddev of total value variation as fraction of total weight)
        :rtype: float
        """
        w = np.array([weights[t] for t in self.prices.columns])
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

    def share_count(self, total, weights):
        """ Determines integer number of shares that should be bought from
        portfolio weights and total portfolio value

        :param total: Total portfolio value
        :type total: float
        :param weights: The weight of each asset in the portfolio
        :type weights: OrderedDict[str, float]

        :return: Each asset mapped to how many shares should be bought
        :rtype: Dict[str, int]
        """
        return {k: int(((v * total) / self.curr_prices[k]).iloc[0]) for k, v in weights.items()}

    def historical_performance(self, weights):
        """ Calculates portfolio performance over the past year
        for the given portfolio weights

        :param weights: The weight of each asset in the portfolio
        :type weights: OrderedDict[str, float]

        :return: The value of the portfolio at every time step
                 The starting portfolio has a value of 1
        :rtype: pandas.Series, indexed by pandas.Timestamp
        """
        trade_days_in_year = 253
        year_performance = self.prices.tail(trade_days_in_year).pct_change()
        weights_array = np.array([weights[t] for t in self.prices.columns])
        year_performance.iloc[0] = weights_array

        # require percent changes
        for i in range(1, len(year_performance.index)):
            year_performance.iloc[i] = (1 + year_performance.iloc[i]) * year_performance.iloc[i - 1]
        portfolio_perf = year_performance.apply(sum, axis=1)
        return portfolio_perf
