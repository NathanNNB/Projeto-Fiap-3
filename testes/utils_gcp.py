# db/gcp_utils.py

import pandas as pd
from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
import os

def salvar_em_bucket(df: pd.DataFrame, bucket_name: str, blob_name: str):
    """Salva um DataFrame como CSV em um bucket do GCP."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

def carregar_csv_para_bigquery(project_id: str, dataset_id: str, table_name: str, bucket_name: str, blob_name: str):
    """Carrega um CSV do bucket para uma tabela do BigQuery."""
    uri = f"gs://{bucket_name}/{blob_name}"
    client = bigquery.Client(project=project_id)

    table_id = f"{project_id}.{dataset_id}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Espera o job terminar

def verificar_ou_criar_dataset(project_id: str, dataset_id: str):
    """Verifica se o dataset existe no BigQuery, senão cria."""
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)

    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        client.create_dataset(dataset)

def verificar_ou_criar_tabela(project_id: str, dataset_id: str, table_name: str, schema: list):
    """Cria a tabela com schema definido, se ela ainda não existir."""
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.{dataset_id}.{table_name}"

    try:
        client.get_table(table_id)
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table)

def ler_tabela_bigquery(project_id: str, dataset_id: str, table_name: str) -> pd.DataFrame:
    """Lê uma tabela do BigQuery e retorna como DataFrame."""
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}`"
    try:
        return client.query(query).to_dataframe()
    except NotFound:
        return pd.DataFrame()
