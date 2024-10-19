""" Routes for core trader functionality.
All route responses should have a "status" field.
"""

from flask import Blueprint, jsonify, request
from flask_cors import CORS
from util import require_json_params
from services.returns import Carhart4FactorModel
from services.model import Model, TickerException

core_blueprint = Blueprint("core", __name__, url_prefix="/")
CORS(core_blueprint)
returns_model = Carhart4FactorModel()


@core_blueprint.route("healthcheck")
def healthcheck():
    """ Always returns 200 OK """
    return jsonify({ "status": "OK" })


@core_blueprint.put("model")
@require_json_params(["value", "tickers"])
def get_weights():
    """ Returns the desired weight of each stock.

    :param value: The total value of the portfolio in USD
    :type value: float
    :param tickers: The tickers to create the portfolio over
    :type tickers: str[]
    """
    body = request.get_json()
    value = body["value"]
    tickers = list(map(lambda t: t.upper(), body["tickers"]))

    try:
        model = Model(returns_model, tickers)
    except TickerException as e:
        return jsonify({
            "status": "ERROR",
            "error": e.message
            }), 400

    print(model) # NO LOGGER 💀
    portfolio = model.max_sharpe(risk_free_rate=model.risk_free_rate)
    returns = (model.portfolio_returns(portfolio) - 1) * value
    volatility = model.portfolio_risk(portfolio)
    sharp = model.sharpe_ratio(portfolio)
    shares = model.share_count(value, portfolio)

    return jsonify({
        "status": "OK",
        "weights": portfolio,
        "shares": shares,
        "return": returns,
        "volatility": volatility,
        "sharpe": sharp
        })
