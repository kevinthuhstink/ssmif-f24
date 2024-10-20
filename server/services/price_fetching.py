""" Utility function to get price data from both yfinance and preexisting data in sql. """

import datetime
import yfinance as yf
import pandas as pd
from . import sql
from .errors import TickerException

def fetch_prices(con, symbols):
    """ Gets the last 2 years of price data for a symbol.
    First checks sql db if the data already exists; then fetches
    all the necessary missing data from yfinance to complete the
    2 year period.

    :param con: Active database connection.
    :type con: sqlite3.Connection
    :param symbols: Tickers to fetch price data for.
    :type symbols: str[]

    :return: DataFrame where each column is the ticker
    :rtype: pandas.DataFrame, indexed by pandas.Timestamp
    """
    recent_entries = list(map(lambda t: sql.find_recent_entry(con, t), symbols))
    if None in recent_entries:
        start_date = datetime.date.today() - datetime.timedelta(days=730)
    else:
        start_date = min(recent_entries)

    try:
        print(f"\nDownloading price data for {symbols}")
        new_data = yf.download(symbols, start=start_date)["Close"].tz_localize(None)
    except Exception as e:
        raise TickerException(f"Fetching price data for {symbols} failed", symbols) from e

    # If only one ticker is requested, yfinance returns pd.Series instead of pd.DataFrame
    if len(symbols) == 1:
        new_data = pd.DataFrame(new_data)
        new_data.columns = symbols

    print(new_data)
    for ticker in new_data:
        if new_data[ticker].empty or new_data[ticker].isna().any():
            raise TickerException(f"Price data for ticker ${ticker.upper()} is missing.", ticker)

    sql.insert_price_data(con, new_data)
    return pd.concat(map(lambda t: sql.get_price_data(con, t), symbols), axis=1)
