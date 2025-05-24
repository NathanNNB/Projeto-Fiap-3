import os
from app import create_app
from flask_cors import CORS
from flask import request, redirect

app = create_app()

env = os.environ.get('ENV', 'local') 

@app.before_request
def before_request():
    # If the request is NOT secure (not HTTPS)
    if not request.is_secure and env != 'local':
        # Build the HTTPS version of the URL
        url = request.url.replace("http://", "https://", 1)
        # Redirect to HTTPS URL with permanent redirect status code 301
        return redirect(url, code=301)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))

    if env == 'local':
        # Rodando localmente
        print("Running in LOCAL environment")
        app.run(host='0.0.0.0', port=port, debug=True)  # debug ativo localmente
    else:
        # Rodando no GCP (produção)
        print("Running in PRODUCTION environment")
        app.run(host='0.0.0.0', port=port)

