""" Commmon utility functions used in request routes """

from functools import wraps
from flask import request, jsonify

def require_json_params(params):
    """ Checks if the request query string has necessary parameters.
    Returns a 401 response if any query params are absent.

    :param query_args: A list of body parameter names.
    :type query_args: str[]
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context = request.get_json()
            for i in params:
                if context.get(i) is None:
                    return jsonify({
                        "status": "failure", "reason": f"Missing JSON body param {i}"
                    })
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_query_params(query_args):
    """ Checks if the request query string has necessary parameters.
    Returns a 401 response if any query params are absent.

    :param query_args: A list of query parameter names.
    :type query_args: str[]
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in query_args:
                if request.args.get(i) is None:
                    return jsonify({
                        "status": "failure", "reason": f"Missing query string param {i}"
                    })
            return func(*args, **kwargs)
        return wrapper
    return decorator
