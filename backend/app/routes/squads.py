from flask import Blueprint, jsonify
from app.services.squads import squadsList
from flask_cors import CORS
from dotenv import load_dotenv
from google.cloud import bigquery\

# Carrega as variáveis do arquivo .env
load_dotenv()

squads = Blueprint("squads", __name__)
CORS(squads)

@squads.route("/", methods=["GET"])

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
        formations = squadsList

    return jsonify({"squads": formations})