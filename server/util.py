""" Commmon utility functions used in request routes """

from functools import wraps
from flask import request, jsonify
from jwt import InvalidTokenError, ExpiredSignatureError
from services.auth import decode_jwt

def require_json_params(params):
    """ Checks if the request query string has necessary parameters.
    Returns a 400 response if any query params are absent.

    :param params: A list of body parameter names.
    :type params: str[]
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            context = request.get_json()
            for i in params:
                if context.get(i) is None:
                    return jsonify({
                        "status": "failure", "error": f"Missing JSON body param {i}"
                    }), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_authentication(func):
    """ Checks if the request has a valid JWT token in the Authentication header
    Returns a 444 response if token verification fails
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            auth = request.headers["Authorization"]
            decode_jwt(auth)
            return func(*args, **kwargs)
        except ExpiredSignatureError:
            return jsonify({
                "status": "failure",
                "error": "Invalid auth credentials: Token expired, please reauthenticate"
            }), 444
        except InvalidTokenError:
            return jsonify({
                "status": "failure",
                "error": "Invalid auth credentials: JWT verification failed"
            }), 444
    return wrapper
