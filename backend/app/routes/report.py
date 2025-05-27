import os
import joblib
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from google.cloud import bigquery
import numpy as np

# Pega o diretório do arquivo atual (por exemplo, sua rota)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "modelo", "modelo_random_forest_dupla_entrada.pkl"))

print(f"Carregando modelo de: {MODEL_PATH}")
modelo = joblib.load(MODEL_PATH)
report = Blueprint("report", __name__)
CORS(report)

@report.route("/", methods=["GET"])
def list_report():
    client = bigquery.Client()

    # Pega o opponent_id da query string
    opponent_id = request.args.get("opponent_id", type=int)
    visitor = request.args.get("field", type=int)

    if opponent_id is None:
        return jsonify({"error": "Missing opponent_id parameter"}), 400

    query = """
        SELECT  
            team_id,
            ANY_VALUE(team_name) AS team_name,
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

    prediction_query = """
        with estatisticas_team AS (
  SELECT 
  distinct
    team_id,
    rodada,
    elo_team AS elo_team_rodada_anterior,
    AVG(`total_gols`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_goals_team,
    AVG(`total_gols_contra`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_goals_contra_team,
    AVG(`Total Shots`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_shots_team,
    AVG(`Shots on Goal`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_shots_on_goal_team,
    AVG(`Ball Possession`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_possession_team,
    AVG(`expected_goals`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_expected_goals_team,
    AVG(`Passes accurate`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_passes_accurate_team,
    AVG(`Total passes`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_passes_team,
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 1) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 0 PRECEDING AND 0 PRECEDING
) +
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.8) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
) +
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.6) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 2 PRECEDING AND 2 PRECEDING
)+
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.4) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 3 PRECEDING AND 3 PRECEDING
  )  +
  SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.2) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 4 PRECEDING
) AS form_score_weighted_team,



        SUM(case when result = 2 and flag_casa = 1 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) / sum(case when flag_casa = 1 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) as win_rate_home_team,
    SUM(case when result = 2 and flag_casa = 0 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) / sum(case when flag_casa = 0 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) as win_rate_away_team
  FROM `fut.dados_partidas_trat_elo`
  where team_id = @team1
),

estatisticas_opp AS (
  SELECT 
  distinct
    team_id AS opponent_id,
    rodada,
    elo_team AS elo_opp_rodada_anterior,
    AVG(`total_gols`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_goals_opp,
    AVG(`total_gols_contra`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_goals_contra_opp,
    AVG(`Total Shots`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_shots_opp,
    AVG(`Shots on Goal`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_shots_on_goal_opp,
    AVG(`Ball Possession`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_possession_opp,
        AVG(`expected_goals`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_expected_goals_opp,
            AVG(`Passes accurate`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_passes_accurate_opp,
    AVG(`Total passes`) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 0 PRECEDING) AS avg_total_passes_opp,
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 1) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 0 PRECEDING AND 0 PRECEDING
) +
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.8) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
) +
SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.6) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 2 PRECEDING AND 2 PRECEDING
) + SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.4) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 3 PRECEDING AND 3 PRECEDING
)+ SUM(CASE WHEN result = 2 THEN 3 WHEN result = 1 THEN 1 ELSE 0 END * 0.2) OVER (
  PARTITION BY team_id ORDER BY rodada ROWS BETWEEN 4 PRECEDING AND 4 PRECEDING
)AS form_score_weighted_opp,


    SUM(case when result = 2 and flag_casa = 1 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) / sum(case when flag_casa = 1 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) as win_rate_home_opp,
    SUM(case when result = 2 and flag_casa = 0 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) / sum(case when flag_casa = 0 then 1 end) OVER (PARTITION BY team_id ORDER BY rodada ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) as win_rate_away_opp

  FROM `fut.dados_partidas_trat_elo`
  where team_id = @team2 
),

final AS (
  SELECT 
        et.team_id,
        eo.opponent_id,
        -- lembrar de ver qual variavel usar
    et.win_rate_home_team,
    et.win_rate_away_team,
        et.elo_team_rodada_anterior,
        -- Features do time
        et.avg_total_goals_team,
        (et.avg_total_goals_contra_team) * -1 as avg_total_goals_contra_team,
        et.avg_total_shots_team,
        et.avg_shots_on_goal_team,
        et.avg_possession_team,
        et.avg_expected_goals_team,
        -- Features do adversário
    eo.win_rate_away_opp,
    eo.win_rate_home_opp,
        eo.elo_opp_rodada_anterior,
        eo.avg_total_goals_opp,
        (eo.avg_total_goals_contra_opp) * -1 as avg_total_goals_contra_opp,
        eo.avg_total_shots_opp,
        eo.avg_shots_on_goal_opp,
        eo.avg_possession_opp,
        eo.avg_expected_goals_opp,
    et.form_score_weighted_team,
    eo.form_score_weighted_opp
    FROM  estatisticas_team et
    CROSS JOIN estatisticas_opp eo
        WHERE et.rodada = 38 and eo.rodada = 38
    )
    SELECT distinct *
    FROM final
    """

    job_config_prediction = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("team1", "INT64", 33),
            bigquery.ScalarQueryParameter("team2", "INT64", opponent_id),
        ]
    )

    df = client.query(prediction_query, job_config=job_config_prediction).to_dataframe()
    df = df.assign(contextual_home_score_team = lambda df: np.where(visitor == 1, df.win_rate_home_team,df.win_rate_away_opp),contextual_home_score_opp = lambda df: np.where(visitor == 1, df.win_rate_away_opp,df.win_rate_home_opp))[['contextual_home_score_team',
             'avg_total_goals_team',
       'avg_total_shots_team',
         'avg_shots_on_goal_team',
          'avg_possession_team',
       'avg_expected_goals_team',
         'contextual_home_score_opp',
           'elo_team_rodada_anterior',
           'elo_opp_rodada_anterior',
       'avg_total_goals_opp',
         'avg_total_shots_opp',
           'avg_shots_on_goal_opp',
       'avg_possession_opp',
         'avg_expected_goals_opp',
       'form_score_weighted_team',
         'form_score_weighted_opp']]
    y_proba = modelo.predict_proba(df)

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Cria uma lista com os dados dos dois times
    teams_data = [dict(row.items()) for row in results]

    return jsonify({"teams": teams_data, "victoryData": y_proba.tolist()})