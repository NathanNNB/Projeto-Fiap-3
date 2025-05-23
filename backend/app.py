import os
from app import create_app
from flask_cors import CORS

app = create_app()
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    env = os.environ.get('ENV', 'local')  # default é local

    if env == 'local':
        # Rodando localmente
        print("Running in LOCAL environment")
        app.run(host='0.0.0.0', port=port, debug=True)  # debug ativo localmente
    else:
        # Rodando no GCP (produção)
        print("Running in PRODUCTION environment")
        app.run(host='0.0.0.0', port=port)