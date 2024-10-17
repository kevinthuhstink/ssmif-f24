""" Retrieves the factors used in the Carhart 4-factor model """

import datetime
import pandas as pd
import yfinance as yf

TRADEDAYS_IN_YEAR = 252

def risk_free_rates():
    pass


def market_rates():
    """ Returns the 12-month S&P return for every day
    over the last 12 months.
    :rtype: pandas.Series
    """
    snp = yf.Ticker("^GSPC").history(period="2y")["Close"].tz_localize(None)
    year_ago = snp.loc[:snp.index[252]]
    this_year = snp.loc[snp.index[-253]:]

    date_indices = this_year.index
    year_ago.index = list(range(TRADEDAYS_IN_YEAR + 1))
    this_year.index = list(range(TRADEDAYS_IN_YEAR + 1))

    market_returns = this_year / year_ago
    market_returns.index = date_indices
    market_returns.name = "r_m"
    return market_returns
