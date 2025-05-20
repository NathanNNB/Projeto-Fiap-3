# Estrutura modularizada com integração ao GCP
from fastapi import FastAPI, Query
from typing import Optional
from dotenv import load_dotenv
import logging
import os
import time
import pandas as pd
from google.cloud import storage, bigquery
from api_requests import make_request
from dados_api import buscar_times, buscar_partidas, buscar_estatisticas, buscar_lineups
from utils_gcp import (
    salvar_em_bucket,
    verificar_ou_criar_dataset,
    verificar_ou_criar_tabela,
    carregar_csv_para_bigquery,
    ler_tabela_bigquery
)

app = FastAPI()
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BUCKET_NAME = os.getenv("GCP_BUCKET")
BQ_DATASET = os.getenv("BQ_DATASET")
PROJECT_ID = os.getenv("GCP_PROJECT")

@app.on_event("startup")
def startup():
    verificar_ou_criar_dataset(PROJECT_ID, BQ_DATASET)

@app.get("/coletar_dados")
def coletar_dados(season: str = Query(...), league: str = Query(...)):
    token = os.getenv("API_TOKEN")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': token
    }

    logging.info("Início do processo de coleta de dados...")

    df_teams = ler_tabela_bigquery(PROJECT_ID, BQ_DATASET, "teams")
    df_partidas = ler_tabela_bigquery(PROJECT_ID, BQ_DATASET, "partidas")
    df_stats = ler_tabela_bigquery(PROJECT_ID, BQ_DATASET, "estatisticas")
    df_lineups = ler_tabela_bigquery(PROJECT_ID, BQ_DATASET, "lineups")

    if df_teams.empty and df_partidas.empty:
        logging.info("Bases ausentes, iniciando coleta total.")
        df_teams = buscar_times(headers, season, league)
        salvar_em_bucket(df_teams, BUCKET_NAME, "teams_info.csv")
        carregar_csv_para_bigquery(PROJECT_ID, BQ_DATASET, "teams", BUCKET_NAME, "teams_info.csv")

        all_matches = []
        for team_id in df_teams['team_id']:
            partidas = buscar_partidas(team_id, season, league, headers)
            all_matches.append(partidas)
        df_partidas = pd.concat(all_matches)
        salvar_em_bucket(df_partidas, BUCKET_NAME, "df_partidas.csv")
        carregar_csv_para_bigquery(PROJECT_ID, BQ_DATASET, "partidas", BUCKET_NAME, "df_partidas.csv")

    times_incompletos = [t for t in df_partidas['team_id'].unique() if df_partidas[df_partidas['team_id'] == t].shape[0] < 38]
    if times_incompletos:
        logging.info(f"Encontrados times com menos de 38 partidas: {times_incompletos}")
        for team_id in times_incompletos:
            novas_partidas = buscar_partidas(team_id, season, league, headers)
            df_partidas = pd.concat([df_partidas, novas_partidas]).drop_duplicates('id_partida')
        salvar_em_bucket(df_partidas, BUCKET_NAME, "df_partidas.csv")
        carregar_csv_para_bigquery(PROJECT_ID, BQ_DATASET, "partidas", BUCKET_NAME, "df_partidas.csv")

    ids_partidas = set(df_partidas['id_partida'])
    ids_stats = set(df_stats['id_partida']) if not df_stats.empty else set()
    ids_lineups = set(df_lineups['id_partida']) if not df_lineups.empty else set()

    faltam_stats = list(ids_partidas - ids_stats)
    faltam_lineups = list(ids_partidas - ids_lineups)

    if not faltam_stats and not faltam_lineups:
        logging.info("Todos os dados já estão completos para a temporada.")
    else:
        logging.info(f"Buscando estatísticas para {len(faltam_stats)} partidas e lineups para {len(faltam_lineups)} partidas")
        novas_stats = []
        novas_lineups = []

        for partida_id in set(faltam_stats + faltam_lineups):
            if partida_id in faltam_stats:
                stats = buscar_estatisticas(partida_id, headers)
                novas_stats.append(stats)
                time.sleep(1)
            if partida_id in faltam_lineups:
                lineups = buscar_lineups(partida_id, headers)
                novas_lineups.append(lineups)
                time.sleep(1)

        if novas_stats:
            df_stats = pd.concat([df_stats] + novas_stats)
            salvar_em_bucket(df_stats, BUCKET_NAME, "df_stats.csv")
            carregar_csv_para_bigquery(PROJECT_ID, BQ_DATASET, "estatisticas", BUCKET_NAME, "df_stats.csv")

        if novas_lineups:
            df_lineups = pd.concat([df_lineups] + novas_lineups)
            salvar_em_bucket(df_lineups, BUCKET_NAME, "df_lineups.csv")
            carregar_csv_para_bigquery(PROJECT_ID, BQ_DATASET, "lineups", BUCKET_NAME, "df_lineups.csv")

    return {"status": "Processo finalizado com sucesso."}
