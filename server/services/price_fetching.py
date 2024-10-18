""" Utility function to get price data from both yfinance and preexisting data in sql. """

import datetime
import yfinance as yf
import pandas as pd
from . import sql

def fetch_prices(symbols):
    """ Gets the last 2 years of price data for a symbol.
    First checks sql db if the data already exists; then fetches
    all the necessary missing data from yfinance to complete the
    2 year period.

    :param symbols: Tickers to fetch price data for.
    :type symbols: str[]

    :return: DataFrame where each column is the ticker
    :rtype: pandas.DataFrame, indexed by pandas.Timestamp
    """
    recent_entries = list(map(sql.find_recent_entry, symbols))
    if None in recent_entries:
        start_date = datetime.date.today() - datetime.timedelta(days=730)
    else:
        start_date = min(recent_entries)
    print(start_date)
    new_data = yf.download(symbols, start=start_date)["Close"].tz_localize(None)
    if len(symbols) == 1:
        new_data = pd.DataFrame(new_data)
        new_data.columns = symbols
    sql.insert_price_data(new_data)
    return pd.concat(map(sql.get_price_data, symbols), axis=1)
