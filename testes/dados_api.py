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
    return pd.DataFrame([{
        "team_id": t["team"]["id"],
        "nome": t["team"]["name"],
        "pais": t["team"]["country"],
        "temporada": season,
        "liga": league
    } for t in data["response"]])

def buscar_partidas(team_id, season, league, headers):
    path = f"/fixtures?season={season}&league={league}&team={team_id}"
    data = make_request(path, headers)
    if not data:
        return pd.DataFrame()
    return pd.DataFrame([{
        "id_partida": f["fixture"]["id"],
        "data": f["fixture"]["date"],
        "time_casa": f["teams"]["home"]["id"],
        "time_fora": f["teams"]["away"]["id"],
        "gols_casa": f["goals"]["home"],
        "gols_fora": f["goals"]["away"]
    } for f in data["response"]])

def buscar_estatisticas(match_id, headers):
    path = f"/fixtures/statistics?fixture={match_id}"
    data = make_request(path, headers)
    if not data:
        return pd.DataFrame()
    stats = []
    for s in data["response"]:
        for stat in s["statistics"]:
            stats.append({
                "id_partida": match_id,
                "time_id": s["team"]["id"],
                "tipo": stat["type"],
                "valor": stat["value"]
            })
    return pd.DataFrame(stats)

def buscar_lineups(match_id, headers):
    path = f"/fixtures/lineups?fixture={match_id}"
    data = make_request(path, headers)
    if not data:
        return pd.DataFrame()
    lineups = []
    for l in data["response"]:
        lineups.append({
            "id_partida": match_id,
            "time_id": l["team"]["id"],
            "tecnico": l["coach"]["name"] if l.get("coach") else None,
            "formacao": l.get("formation"),
            "jogadores": str(l.get("startXI"))
        })
    return pd.DataFrame(lineups)
