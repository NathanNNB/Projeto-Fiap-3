# services/dados_api.py
import pandas as pd
import time
import logging
from api_requests import make_request

def buscar_times(headers, season, league):
    path = f"/teams?season={season}&league={league}"
    data = make_request(path, headers)
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

def buscar_partidas(team_id, season, league, headers):
    path = f"/fixtures?season={season}&league={league}&team={team_id}"
    data = make_request(path, headers)
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

def buscar_estatisticas(match_id, headers):
    path = f"/fixtures/statistics?fixture={match_id}"
    data = make_request(path, headers)
    if not data:
        return pd.DataFrame()
    estatisticas = []
    for team_data in data['response']:
        estatisticas_time = {item['type']: item['value'] for item in team_data['statistics']}
        estatisticas_time['time'] = team_data['team']['name']
        estatisticas_time['id_time'] = team_data['team']['id']
        estatisticas_time['fixture_id'] = match_id
        estatisticas.append(estatisticas_time)
    df_estatisticas = pd.DataFrame(estatisticas)
    cols = ['fixture_id', 'id_time', 'time'] + [col for col in df_estatisticas.columns if col not in ['fixture_id', 'id_time', 'time']]
    return df_estatisticas[cols]

def buscar_lineups(match_id, headers):
    path = f"/fixtures/lineups?fixture={match_id}"
    data = make_request(path, headers)
    if not data:
        return pd.DataFrame()
    lineups = []
    for l in data["response"]:
        lineups.append({
            "id_partida": match_id,
            "id_time": l["team"]["id"],
            "coach": l["coach"]["name"] if l.get("coach") else None,
            "formation": l.get("formation")
        })
    df_lineups = pd.DataFrame(lineups)
    cols = ['fixture_id', 'id_time', 'time'] + [col for col in df_lineups.columns if col not in ['fixture_id', 'id_time', 'time']]
    return df_lineups[cols]
