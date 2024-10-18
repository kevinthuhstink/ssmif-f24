""" Retrieves the factors used in the Carhart 4-factor model """

import datetime
from functools import reduce
import pandas as pd
import yfinance as yf
from . import sql

TRADEDAYS_IN_YEAR = 252

class FactorModel():
    """ Produces the factors used in the Carhart 4-factor model """
    def __init__(self, tickers=None):
        if tickers:
            self.tickers = tickers
        else:
            self.tickers = {
                    "small_value": ["EVRI", "AVD", "HDSN"],
                    "small_growth": ["ACMR", "LRN", "DGII"],
                    "big_value": ["NKE", "PFE", "UPS", "USB"],
                    "big_growth": ["AMZN", "CRM"],
                    "winners": ["NVDA", "COHR", "APP", "MSTR"],
                    "losers": ["NFE", "NYCB", "MBLY"]
                    }
        prices = {k: FactorModel.get_prices(v).dropna(axis=1) for k, v in self.tickers.items()}

        # Price history aggregated for the entire "category"
        self.prices_agg = {k: v.sum(axis=1) for k, v in prices.items()}
        # print(self.prices_agg)
        self.rates_agg = {k: _12mo_return_rate(v) for k, v in self.prices_agg.items()}
        # print(self.rates_agg)

    @staticmethod
    def get_prices(symbols):
        """ Gets the last 2 years of price data for a symbol. """
        recent_entries = list(filter(lambda x: x is not None, map(sql.find_recent_entry, symbols)))
        start_date = datetime.date.today() - datetime.timedelta(days=730)
        if len(recent_entries) > 0:
            start_date = min(recent_entries)
        new_data = yf.download(symbols, start=start_date)["Close"].tz_localize(None)
        sql.insert_price_data(new_data)
        return pd.concat(map(sql.get_price_data, symbols), axis=1)

    def smb(self):
        """ Gives the "small minus big" advantage for every day
        over the last 12 months.
        Advantage is calculated by the small_value's 12-month rate
        subtracted by the big_value's 12-month rate

        :rtype: pandas.Series, indexed by pandas.Timestamp
        """
        smb_advantage = self.rates_agg["small_value"] - self.rates_agg["big_value"]
        smb_advantage.name = "SMB"
        return smb_advantage

    def hml(self):
        """ Gives the "high minus low" advantage for every day
        over the last 12 months.
        Advantage is calculated by the return rate of the value assets
        subtracted by the return rate of the growth assets

        :rtype: pandas.Series, indexed by pandas.Timestamp
        """
        value_prices = self.prices_agg["big_value"] + self.prices_agg["small_value"]
        growth_prices = self.prices_agg["big_growth"] + self.prices_agg["small_growth"]
        value_rates = _12mo_return_rate(value_prices)
        growth_rates = _12mo_return_rate(growth_prices)
        hml_advantage = value_rates - growth_rates
        hml_advantage.name = "HML"
        return hml_advantage

    def umd(self):
        """ Gives the "up minus down" advantage for every day
        over the last 12 months.
        Advantage is calculated by the winners' 12-month rate
        subtracted by the losers' 12-month rate
        """
        umd_advantage = self.rates_agg["winners"] - self.rates_agg["losers"]
        umd_advantage.name = "UMD"
        return umd_advantage


def risk_free_rates():
    """ Returns the risk-free rate, based on the 13wk treasury bill
    interest rate for every day over the last 12 months.

    :rtype: pandas.Series, indexed by pandas.Timestamp
    """
    irx = yf.Ticker("^IRX").history(period="1y")["Close"].tz_localize(None)
    irx.name = "Risk Free Rate"
    irx = irx.map(lambda x: 1 + x / 100)
    return irx


def market_rates():
    """ Returns the 12-month S&P return rate for every day
    over the last 12 months.

    :rtype: pandas.Series, indexed by pandas.Timestamp
    """
    snp = yf.Ticker("^GSPC").history(period="2y")["Close"].tz_localize(None)
    market_returns = _12mo_return_rate(snp)
    market_returns.name = "Market Returns"
    return market_returns


def _12mo_return_rate(prices):
    """ Takes a 2yr series of returns, and gives the 12-month
    change (return rate) for every day in the last year.

    :param prices: Asset prices over the past 2 years.
    :type prices: pandas.Series, indexed by pandas.Timestamp

    :return: The annualized asset return rate for every day of the last year.
             Contains data for 253 trading days.
    :rtype: pandas.Series, indexed by pandas.Timestamp
    """
    num_days = TRADEDAYS_IN_YEAR
    this_year = prices.loc[:prices.index[num_days]]
    last_year = prices.loc[prices.index[-1 * num_days - 1]:]

    date_indices = this_year.index
    last_year.index = list(range(num_days + 1))
    this_year.index = list(range(num_days + 1))

    rates = this_year / last_year
    rates.index = date_indices
    return rates
