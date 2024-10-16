""" Server runner """

from flask import Flask
from flask_cors import CORS
from routes.core import core_blueprint
from config import PORT

def init_app():
    """ Creates a flask server instance. """
    app = Flask(__name__)
    app.register_blueprint(core_blueprint)
    CORS(app)
    return app

if __name__ == "__main__":
    server = init_app()
    server.run(host="0.0.0.0", port=PORT)
