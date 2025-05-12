# utils/api_requests.py
import http.client
import json
import logging
import time


def make_request(path: str, headers: dict, retries=3, delay=5):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    for attempt in range(retries):
        try:
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()

            if res.status == 499:
                logging.error("Erro 499: Limite de uso da API atingido.")
                raise Exception("Limite de uso da API atingido.")
            elif res.status == 500:
                logging.error("Erro 500: Internal Server Error.")
                raise Exception("Internal Server Error.")
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
