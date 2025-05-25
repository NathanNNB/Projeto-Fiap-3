from flask import Blueprint, jsonify, request
from flask_cors import CORS
from google.cloud import bigquery

report = Blueprint("report", __name__)
CORS(report)

@report.route("/", methods=["GET"])
def list_report():
    client = bigquery.Client()

    # Pega o opponent_id da query string
    opponent_id = request.args.get("opponent_id", type=int)

    if opponent_id is None:
        return jsonify({"error": "Missing opponent_id parameter"}), 400

    query = """
        SELECT
            team_id,
            ROUND(AVG(CAST(avg_total_goals_team AS FLOAT64)), 2) AS avg_total_goals_team,
            ROUND(AVG(CAST(avg_shots_on_goal_team AS FLOAT64)), 2) AS avg_shots_on_goal_team,
            ROUND(AVG(CAST(avg_possession_team AS FLOAT64)), 2) AS avg_possession_team,
            ROUND(AVG(CAST(avg_expected_goals_team AS FLOAT64)), 2) AS avg_expected_goals_team,
            ROUND(AVG(CAST(avg_passes_accurate_team AS FLOAT64)), 2) AS avg_passes_accurate_team,
            ROUND(AVG(CAST(avg_total_passes_team AS FLOAT64)), 2) AS avg_total_passes_team
        FROM `fiap-3.fut.dados_estatisticas_gerais`
        WHERE team_id IN (@team1, @team2)
        GROUP BY team_id
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("team1", "INT64", 33),
            bigquery.ScalarQueryParameter("team2", "INT64", opponent_id),
        ]
    )

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Cria uma lista com os dados dos dois times
    teams_data = [dict(row.items()) for row in results]

    return jsonify({"teams": teams_data})