""" Database services, mainly to store price data. """

import sqlite3
from contextlib import closing
import pandas as pd

con = sqlite3.Connection("prices.db")

def check_table(ticker):
    """ Checks if the ticker has an existing db table. """
    cur = con.cursor()
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ticker}'")
    res = cur.fetchone()
    cur.close()
    return bool(res)


def find_recent_entry(ticker, limit=750):
    """ Finds the most recent existing data entry for a ticker.

    :param ticker: Ticker name, all uppercase
    :type ticker: str
    :param limit: Max number of days to check for until the program times out
    :type limit: int

    :return: The timestmap of the first date that has data for the ticker.
             Returns None if the table has no data or limit was reached
             before data was found.
    :rtype: pandas.Timestamp | None
    """
    with closing(con.cursor()) as cur:
        if not check_table(ticker):
            return None

        today = pd.Timestamp.today().round(freq="d")
        while limit > 0:
            timestamp = int(today.timestamp())
            cur.execute(f"SELECT price FROM {ticker} WHERE t={timestamp}")
            if cur.fetchone():
                return today
            today = today - pd.Timedelta(1, "day")
            limit -= 1
        return None


def insert_price_data(df):
    """ Inserts a dataframe of price data into the database.

    :param df: DataFrame with ticker columns and price entries.
    :type df: pandas.DataFrame, indexed by pandas.Timestamp
    """
    with closing(con.cursor()) as cur:
        for ticker in df:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {ticker} (t INTEGER PRIMARY KEY, price REAL)")
            prices = df[ticker]
            for t, price in prices.items():
                timestamp = int(t.timestamp())
                cur.execute(f"INSERT OR REPLACE INTO {ticker} VALUES (?, ?)", (timestamp, price))


def get_price_data(ticker, start=pd.Timestamp.today().round(freq="d"), days=750):
    """ Gets all price entries within a day range.

    :param ticker: Ticker name, all uppercase, table to query
    :type ticker: str
    :param start: The first day to get db data for
    :type start: pandas.Tiemstamp
    :param days: Number of days to get db data for
    :type days: int

    :return: Time series with all available data for the period
    :rtype: pandas.Series, indexed by pandas.Timestamp
    """
    with closing(con.cursor()) as cur:
        if not check_table(ticker):
            return pd.Series()

        day_to_get = start - pd.Timedelta(days, "d")
        data = pd.Series()
        while day_to_get <= start:
            time = day_to_get.timestamp()
            res = cur.execute(f"SELECT * FROM {ticker} WHERE t={time}").fetchone()
            if res:
                t, price = res
                t = pd.Timestamp.utcfromtimestamp(t).tz_convert(None)
                data[t] = price
            day_to_get = day_to_get + pd.Timedelta(1, "day")
        data.name = ticker
        return data
