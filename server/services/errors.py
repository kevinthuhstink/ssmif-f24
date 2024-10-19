""" Defines common errors while running the model. """

class TickerException(Exception):
    """ Has class variable self.ticker so you know which ticker doesn't work """
    def __init__(self, message, ticker):
        super().__init__(message)
        self.message = message
        self.ticker = ticker
