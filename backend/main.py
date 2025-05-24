import os
from app import create_app
from flask_cors import CORS
from flask import request, redirect
from werkzeug.middleware.proxy_fix import ProxyFix  # 👈 IMPORTANTE

from dotenv import load_dotenv
load_dotenv()

app = create_app()
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # 👈 ESSENCIAL
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def enforce_https():
    if os.getenv("FLASK_ENV") == "production":
        if request.headers.get("X-Forwarded-Proto", "http") != "https":
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=308)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))

    if os.getenv("FLASK_ENV") == "local":
        print("Running in LOCAL environment")
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print("Running in PRODUCTION environment")
        app.run(host='0.0.0.0', port=port)