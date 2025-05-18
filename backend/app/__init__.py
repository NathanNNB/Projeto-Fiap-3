from flask import Flask
from flask_cors import CORS
from .routes.squads import squads
from .routes.opponents import opponents
from .routes.report import report

def create_app():
    app = Flask(__name__)
    
    # TODO Verificar para requests de producao
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    # Registro das rotas

    app.register_blueprint(squads, url_prefix="/squads")
    app.register_blueprint(opponents, url_prefix="/opponents")
    app.register_blueprint(report, url_prefix="/report")

    return app