""" Routes for core trader functionality """

from flask import Blueprint, jsonify, request
from flask_cors import CORS
from util import require_json_params

core_blueprint = Blueprint("core", __name__, url_prefix="/")
CORS(core_blueprint)

@core_blueprint.route("healthcheck")
def healthcheck():
    """ Always returns 200 OK """
    return jsonify({
        "status": "OK"
        })

@core_blueprint.put("weights")
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

    return jsonify({
        "status": "OK",
        "value": value,
        "tickers": tickers
        })
