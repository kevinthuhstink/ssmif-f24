""" Routes for core trader functionality.
All routes should have a "status" field.
"""

from flask import Blueprint, jsonify, request
from flask_cors import CORS
from util import require_json_params
from services.model import Model, TickerException

core_blueprint = Blueprint("core", __name__, url_prefix="/")
CORS(core_blueprint)


@core_blueprint.route("healthcheck")
def healthcheck():
    """ Always returns 200 OK """
    return jsonify({ "status": "OK" })


@core_blueprint.put("model")
@require_json_params(["value", "tickers"])
def portfolio():
    """ Returns the desired weight of each stock.

    :param value: The total value of the portfolio in USD
    :type value: float
    :param tickers: The tickers to create the portfolio over
    :type tickers: str[]
    """
    body = request.get_json()
    value = body["value"]
    tickers = body["tickers"]

    try:
        model = Model(value, tickers)
    except TickerException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
            }), 400

    return jsonify({
        "status": "OK",
        "weights": model(),
        "return": 0,
        "volatility": 0,
        "sharpe": 0
        })
