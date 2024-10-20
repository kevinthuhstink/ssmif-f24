""" JWT creation/decode functions """

import os
from time import time
from jwt import encode, decode

if "JWT_SECRET" not in os.environ:
    raise EnvironmentError("JWT_SECRET is a required environment variable")
SECRET = os.environ["JWT_SECRET"]

def create_jwt():
    """ Creates a JWT that expires in 1 day.
    :rtype: str
    """
    now = int(time())
    exp_1day = 60 * 60 * 24
    return encode({
        "iss": "f24-ssmif-submission",
        "iat": now,
        "exp": now + exp_1day
        }, SECRET, algorithm="HS256")


def decode_jwt(token):
    """ Decodes JWT.
    Throws InvalidSignatureError if JWT verification fails.

    :param token: JWT to decode
    :type token: str

    :return: Decoded JWT payload
    :rtype: Dict[str, unknown]
    """
    return decode(token, SECRET, algorithms="HS256")
