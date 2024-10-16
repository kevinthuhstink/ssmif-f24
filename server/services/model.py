""" The portfolio optimization model. """

import pandas as pd
import yfinance as yf
from pypfopt.risk_models import risk_matrix, fix_nonpositive_semidefinite
from pypfopt.expected_returns import capm_return
from pypfopt.efficient_frontier import EfficientFrontier

class ReturnsModel:
    """ Dummy returns EMA model """
    def __init__(self, prices):
        self.returns = capm_return(prices)

    def __str__(self):
        return str(self.returns)


class Model(EfficientFrontier):
    """ Dummy super basic model """
    def __init__(self, value, tickers):
        self.value = value
        self.tickers = {t: yf.Ticker(t).history(period="1y") for t in tickers}
        closes = pd.DataFrame.from_dict({k: v.get("Close") for k, v in self.tickers.items()})
        self.returns = ReturnsModel(closes).returns
        self.risk = fix_nonpositive_semidefinite(risk_matrix(closes))
        super().__init__(self.returns, self.risk)

    def __str__(self):
        return f"""Covariance:\n{self.risk}\n\n
            Returns:\n{self.returns}\n\n
            Weights\n:{self.max_sharpe()}"""

    def __call__(self, **kwargs):
        if "risk" in kwargs:
            return self.efficient_risk(kwargs["risk"])
        if "return" in kwargs:
            return self.efficient_return(kwargs["return"])
        return self.max_sharpe()
