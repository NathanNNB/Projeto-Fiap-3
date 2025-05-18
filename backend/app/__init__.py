from flask import Flask
from flask_cors import CORS
from .routes.squads import squads
from .routes.opponents import opponents


def create_app():
    app = Flask(__name__)
    CORS(app)  # <--- aqui, liberando o CORS por padrão
    # Registro das rotas

    app.register_blueprint(squads, url_prefix="/squads")
    app.register_blueprint(opponents, url_prefix="/opponents")

    return app