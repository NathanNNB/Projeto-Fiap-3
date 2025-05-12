from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import http.client
import json
import os
import logging
import time
import sys
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()


# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utils

def make_request(path: str, headers: dict, retries=3, delay=5):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    for attempt in range(retries):
        try:
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()
            if res.status == 499:
                logging.error("Erro 499: Limite de uso da API atingido. Interrompendo execução.")
                sys.exit(1)  # ou raise SystemExit
            elif res.status == 500:
                logging.error("Erro 500: Internal Server Error. Verifique a API ou tente mais tarde.")
                raise Exception("Erro 500: Internal Server Error")
            elif res.status != 200:
                logging.error(f"Erro {res.status}: {res.reason}")
                raise Exception(f"Erro {res.status}")
            data = json.loads(res.read().decode("utf-8"))
            if 'response' in data and data['response']:
                return data
        except Exception as e:
            logging.warning(f"Tentativa {attempt+1} falhou: {e}")
        time.sleep(delay)
    return None

# Módulos

def buscar_times(headers: dict, season: str, league: str):
    logging.info("Buscando base de times da API...")
    data = make_request(f"/teams?season={season}&league={league}", headers)
    if not data:
        return pd.DataFrame()

    times = []
    for item in data['response']:
        times.append({
            'team_id': item['team']['id'],
            'team_name': item['team']['name'],
            'team_code': item['team']['code'],
            'team_country': item['team']['country'],
            'founded': item['team']['founded'],
            'is_national': item['team']['is_national'],
            'team_logo': item['team']['logo'],
            'stadium': item['venue']['name'],
            'season': season,
            'league': league
        })
    return pd.DataFrame(times)

def buscar_partidas(id_time: int, season: str, league: str, headers: dict):
    data = make_request(f"/fixtures?season={season}&team={id_time}&league={league}", headers)
    if not data:
        return pd.DataFrame()

    dados_partidas = []
    for partida in data['response']:
        fixture = partida['fixture']
        league = partida['league']
        teams = partida['teams']
        goals = partida['goals']
        score = partida['score']
        dados_partidas.append({
            'data': fixture['date'],
            'id_partida': fixture['id'],
            'rodada': league.get('round'),
            'id_time_casa': teams['home']['id'],
            'time_casa': teams['home']['name'],
            'time_fora': teams['away']['name'],
            'id_time_fora': teams['away']['id'],
            'gols_casa': goals['home'],
            'gols_fora': goals['away'],
            'resultado_intervalo': f"{score['halftime']['home']}x{score['halftime']['away']}",
            'resultado_final': f"{score['fulltime']['home']}x{score['fulltime']['away']}",
            'local': fixture['venue']['name'],
            'cidade': fixture['venue']['city']
        })
    return pd.DataFrame(dados_partidas)

def buscar_estatisticas(id_partida: int, headers: dict):
    data = make_request(f"/fixtures/statistics?fixture={id_partida}", headers)
    if not data:
        return pd.DataFrame()

    estatisticas = []
    for team_data in data['response']:
        estatisticas_time = {item['type']: item['value'] for item in team_data['statistics']}
        estatisticas_time['time'] = team_data['team']['name']
        estatisticas_time['id_time'] = team_data['team']['id']
        estatisticas_time['fixture_id'] = id_partida
        estatisticas.append(estatisticas_time)

    df_stats = pd.DataFrame(estatisticas)
    cols = ['fixture_id', 'id_time', 'time'] + [col for col in df_stats.columns if col not in ['fixture_id', 'id_time', 'time']]
    return df_stats[cols]

def buscar_lineups(id_partida: int, headers: dict):
    data = make_request(f"/fixtures/lineups?fixture={id_partida}", headers)
    if not data:
        return pd.DataFrame()

    lineups = []
    for team_data in data['response']:
        lineups.append({
            'fixture_id': id_partida,
            'id_time': team_data['team']['id'],
            'time': team_data['team']['name'],
            'formation': team_data['formation'],
            'coach': team_data['coach']['name']
        })

    df_lineups = pd.DataFrame(lineups)
    cols = ['fixture_id', 'id_time', 'time'] + [col for col in df_lineups.columns if col not in ['fixture_id', 'id_time', 'time']]
    return df_lineups[cols]
# Rota principal
@app.get("/coletar_dados")
def coletar_dados(season: str = Query(...), league: str = Query(...)):
    token = os.getenv("API_TOKEN")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': token
    }

    logging.info("Início do processo de coleta de dados...")

    # Carregar bases se existirem
    df_teams = pd.read_csv(r'bases\teams_info.csv', sep=';') if os.path.exists(r'bases\teams_info.csv') else pd.DataFrame()
    df_partidas = pd.read_csv(r'bases\df_partidas.csv', sep=';') if os.path.exists(r'bases\df_partidas.csv') else pd.DataFrame()
    df_stats = pd.read_csv(r'bases\df_stats.csv', sep=';') if os.path.exists(r'bases\df_stats.csv') else pd.DataFrame()
    df_lineups = pd.read_csv(r'bases\df_lineups.csv', sep=';') if os.path.exists(r'bases\df_lineups.csv') else pd.DataFrame()

    # 1. Se bases não existirem, iniciar coleta completa
    if df_teams.empty and df_partidas.empty:
        logging.info("Bases ausentes, iniciando coleta total.")
        df_teams = buscar_times(headers, season, league)
        df_teams.to_csv('bases\teams_info.csv', index=False, sep=';')

        all_matches = []
        for team_id in df_teams['team_id']:
            partidas = buscar_partidas(team_id, season, league, headers)
            all_matches.append(partidas)
        df_partidas = pd.concat(all_matches)
        df_partidas.to_csv('bases\df_partidas.csv', index=False, sep=';')

    # 2. Verificar se todos os times possuem 38 partidas
    partidas_por_time = df_partidas['id_time_casa'].value_counts() + df_partidas['id_time_fora'].value_counts()
    times_incompletos = partidas_por_time[partidas_por_time < 38].index.tolist()

    if times_incompletos:
        logging.info(f"Encontrados times com menos de 38 partidas: {times_incompletos}")
        for team_id in times_incompletos:
            novas_partidas = buscar_partidas(team_id, season, league, headers)
            df_partidas = pd.concat([df_partidas, novas_partidas]).drop_duplicates('id_partida')
            df_partidas.to_csv('bases\df_partidas.csv', index=False, sep=';')

    # 3. Verificar quais partidas estão faltando stats/lineups
    partidas_existentes = df_partidas['id_partida'].unique()
    stats_existentes = df_stats['fixture_id'].unique() if not df_stats.empty else []
    lineups_existentes = df_lineups['fixture_id'].unique() if not df_lineups.empty else []

    faltam_stats = list(set(partidas_existentes) - set(stats_existentes))
    faltam_lineups = list(set(partidas_existentes) - set(lineups_existentes))

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
            df_stats.to_csv('bases\df_stats.csv', index=False, sep=';')

        if novas_lineups:
            df_lineups = pd.concat([df_lineups] + novas_lineups)
            df_lineups.to_csv('bases\df_lineups.csv', index=False, sep=';')

    return {"status": "Processo finalizado com sucesso."}
