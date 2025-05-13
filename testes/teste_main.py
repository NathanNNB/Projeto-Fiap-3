# Estrutura modularizada com SQLite em vez de CSV
from fastapi import FastAPI, Query
from typing import Optional
from dotenv import load_dotenv
import logging
import os
import sys
import time
import sqlite3
import pandas as pd
from api_requests import make_request
from dados_api import buscar_times, buscar_partidas, buscar_estatisticas, buscar_lineups
from database import init_db, carregar_base, inserir_dados, partidas_incompletas, partidas_faltantes

app = FastAPI()
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = "dados_futebol.db"
init_db(DB_PATH)

@app.get("/coletar_dados")
def coletar_dados(season: str = Query(...), league: str = Query(...)):
    token = os.getenv("API_TOKEN")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': token
    }

    logging.info("Início do processo de coleta de dados...")

    conn = sqlite3.connect(DB_PATH)
    df_teams = carregar_base(conn, "teams")
    df_partidas = carregar_base(conn, "partidas")
    df_stats = carregar_base(conn, "estatisticas")
    df_lineups = carregar_base(conn, "lineups")

    if df_teams.empty and df_partidas.empty:
        logging.info("Bases ausentes, iniciando coleta total.")
        df_teams = buscar_times(headers, season, league)
        inserir_dados(conn, df_teams, "teams")

        all_matches = []
        for team_id in df_teams['team_id']:
            partidas = buscar_partidas(team_id, season, league, headers)
            all_matches.append(partidas)
        df_partidas = pd.concat(all_matches)
        inserir_dados(conn, df_partidas, "partidas")

    times_incompletos = partidas_incompletas(df_partidas)
    if times_incompletos:
        logging.info(f"Encontrados times com menos de 38 partidas: {times_incompletos}")
        for team_id in times_incompletos:
            novas_partidas = buscar_partidas(team_id, season, league, headers)
            df_partidas = pd.concat([df_partidas, novas_partidas]).drop_duplicates(subset=['id_partida', 'id_time_casa'])
        inserir_dados(conn, df_partidas, "partidas", replace=True)

    faltam_stats, faltam_lineups = partidas_faltantes(df_partidas, df_stats, df_lineups)
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
            inserir_dados(conn, df_stats, "estatisticas", replace=True)

        if novas_lineups:
            df_lineups = pd.concat([df_lineups] + novas_lineups)
            inserir_dados(conn, df_lineups, "lineups", replace=True)

    conn.close()
    return {"status": "Processo finalizado com sucesso."}
