from flask import Flask
from .routes.squads import squads
from .routes.opponents import opponents


def create_app():
    app = Flask(__name__)

    # Registro das rotas

    app.register_blueprint(squads, url_prefix="/squads")
    app.register_blueprint(opponents, url_prefix="/opponents")

    return app