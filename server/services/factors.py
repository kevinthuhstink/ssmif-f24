""" Retrieves the factors used in the Carhart 4-factor model """

from contextlib import closing
import yfinance as yf
from .sql import get_connection
from .price_fetching import fetch_prices

TRADEDAYS_IN_YEAR = 252

class FactorModel():
    """ Produces the factors used in the Carhart 4-factor model """
    def __init__(self, tickers=None):
        with closing(get_connection()) as con:
            if tickers:
                self.tickers = tickers
            else:
                self.tickers = {
                        "small_value": ["EVRI", "AVD", "HDSN"],
                        "small_growth": ["ACMR", "LRN", "DGII"],
                        "big_value": ["NKE", "PFE", "UPS", "USB"],
                        "big_growth": ["AMZN", "CRM"],
                        "winners": ["NVDA", "COHR", "APP", "MSTR"],
                        "losers": ["NFE", "NYCB"]
                        }
            prices = {k: fetch_prices(con, v).dropna(axis=1) for k, v in self.tickers.items()}

        # Price history aggregated for the entire "category"
        self.prices_agg = {k: v.sum(axis=1) for k, v in prices.items()}
        self.rates_agg = {k: m12_return_rate(v) for k, v in self.prices_agg.items()}

    @staticmethod
    def mkt_premium():
        """ Gives the market risk premium for every day
        over the last 12 months.
        Calculated by total market (S&P 500) 12-month returns
        minus the risk-free rate (13-wk treasury bills)

        :rtype: pandas.Series, indexed by pandas.Timestamp
        """
        mkt_prem = market_rates() - risk_free_rates()
        mkt_prem.name = "Mkt. Premium"
        return mkt_prem

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
        value_rates = m12_return_rate(value_prices)
        growth_rates = m12_return_rate(growth_prices)
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
    market_returns = m12_return_rate(snp)
    market_returns.name = "Market Returns"
    return market_returns


def m12_return_rate(prices):
    """ Takes a 2yr series of returns, and gives the 12-month
    change (return rate) for every day in the last year.

    :param prices: Asset prices over the past 2 years.
    :type prices: pandas.Series, indexed by pandas.Timestamp

    :return: The annualized asset return rate for every day of the last year.
             Contains data for 253 trading days.
    :rtype: pandas.Series, indexed by pandas.Timestamp
    """
    num_days = TRADEDAYS_IN_YEAR
    last_year = prices.loc[:prices.index[num_days]]
    this_year = prices.loc[prices.index[-1 * num_days - 1]:]

    date_indices = this_year.index
    last_year.index = list(range(num_days + 1))
    this_year.index = list(range(num_days + 1))

    rates = this_year / last_year
    rates.index = date_indices
    return rates
