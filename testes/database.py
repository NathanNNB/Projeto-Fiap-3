import sqlite3
import pandas as pd
import logging
import os

def init_db(db_path: str):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        logging.info("Banco de dados SQLite criado.")
        conn.close()


def carregar_base(conn: sqlite3.Connection, tabela: str) -> pd.DataFrame:
    try:
        return pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
    except Exception as e:
        logging.warning(f"Tabela {tabela} não encontrada ou vazia: {e}")
        return pd.DataFrame()


def inserir_dados(conn: sqlite3.Connection, df: pd.DataFrame, tabela: str, replace=False):
    if df.empty:
        logging.info(f"DataFrame vazio, não inserido em {tabela}.")
        return
    modo = "replace" if replace else "append"
    df.to_sql(tabela, conn, if_exists=modo, index=False)
    logging.info(f"Dados inseridos na tabela {tabela} com modo {modo}.")


def partidas_incompletas(df_partidas: pd.DataFrame) -> list:
    partidas_por_time = df_partidas.groupby('time_id').size()
    incompletos = partidas_por_time[partidas_por_time < 38].index.tolist()
    return incompletos


def partidas_faltantes(df_partidas: pd.DataFrame, df_stats: pd.DataFrame, df_lineups: pd.DataFrame):
    ids_partidas = set(df_partidas['id_partida'])
    stats_coletadas = set(df_stats['id_partida']) if not df_stats.empty else set()
    lineups_coletados = set(df_lineups['id_partida']) if not df_lineups.empty else set()

    faltam_stats = list(ids_partidas - stats_coletadas)
    faltam_lineups = list(ids_partidas - lineups_coletados)

    return faltam_stats, faltam_lineups
