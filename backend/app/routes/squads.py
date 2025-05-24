import os
from flask import Blueprint, jsonify
from app.services.squads import squadsList
from flask_cors import CORS
from google.cloud import bigquery
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
if os.environ.get("ENV", "local") == "local":
    load_dotenv()

squads = Blueprint("/squads", __name__)
CORS(squads)

@squads.route("", methods=["GET"], strict_slashes=False)

def list_squads():
    client = bigquery.Client()

    query = """
        SELECT DISTINCT formation
        FROM `fut.formacoes`
        WHERE id_time = 33
    """

    try:
        query_job = client.query(query)
        results = query_job.result()

        # Extrai as formações numa lista simples
        formations = [row.formation for row in results]

    except Exception as e:
        print("Not able to get data from DB")
        formations = squadsList

    return jsonify({"squads": formations})