import os
from flask import Blueprint, jsonify
from app.services.opponents import opponentsList
from flask_cors import CORS
from dotenv import load_dotenv
from google.cloud import bigquery\

# Carrega as variáveis do arquivo .env
if os.environ.get("ENV", "local") == "local":
    load_dotenv()

opponents = Blueprint("/opponents", __name__)

CORS(opponents)

@opponents.route("", methods=["GET"], strict_slashes=False)
def list_opponents():
    
    client = bigquery.Client()

    query = """
        SELECT DISTINCT team_name, team_id
        FROM `fiap-3.fut.times`
        WHERE team_name != 'Manchester United'
    """

    try:
        query_job = client.query(query)
        results = query_job.result()

        # Extrai as formações numa lista simples
        opponents_list = [{"team_id": row.team_id, "team_name": row.team_name} for row in results]

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    return jsonify({"opponents": opponents_list})