from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.operators.bash import BashOperator # Não utilizado no exemplo fornecido
import sys
import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Adiciona o diretório src ao PYTHONPATH
# Considerar transformar 'src' em um pacote Python instalável
# ou gerenciar PYTHONPATH via configurações do ambiente Airflow.
sys.path.append('/opt/airflow/src')

from collectors.traffic_collector import get_traffic_data
from collectors.db_utils import insert_traffic_data
from transformers.traffic_transformer import transform_traffic_data, get_traffic_summary

log = logging.getLogger(__name__)

# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def _collect_traffic_data():
    """Coleta dados de trânsito e salva no banco"""
    log.info("Iniciando coleta de dados de trânsito...")
    data = get_traffic_data()
    if data:
        insert_traffic_data(data)
        log.info("Dados de trânsito coletados e salvos com sucesso.")
    else:
        log.warning("Nenhum dado de trânsito foi retornado pelo coletor.")

def _transform_data():
    """Transforma os dados coletados, gera resumo e atualiza status na tabela original."""
    log.info("Iniciando transformação de dados...")
    engine = create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

    # Lê apenas dados não processados das últimas 24 horas (ou todos não processados)
    # A cláusula de tempo (NOW() - INTERVAL '24 hours') é opcional se quiser processar tudo que está pendente.
    # Certifique-se que a tabela traffic_data tem 'id' (PK) e 'is_transformed' (BOOLEAN)
    query = """
    SELECT * FROM traffic_data
    WHERE is_transformed = FALSE AND timestamp >= NOW() - INTERVAL '24 hours'
    ORDER BY timestamp ASC;
    """
    # Se quiser processar todos os não transformados, independentemente da janela:
    # query = "SELECT * FROM traffic_data WHERE is_transformed = FALSE ORDER BY timestamp ASC;"

    df = pd.read_sql(query, engine)

    if not df.empty:
        log.info(f"Transformando {len(df)} novos registros de trânsito.")
        # Transforma os dados
        df_transformed = transform_traffic_data(df.copy()) # Usar .copy() para evitar SettingWithCopyWarning

        # Gera resumo
        summary = get_traffic_summary(df_transformed)

        # Salva dados transformados em uma nova tabela
        df_transformed.to_sql('traffic_data_transformed', engine,
                              if_exists='append', index=False)
        log.info(f"Dados transformados salvos na tabela 'traffic_data_transformed'.")

        # Salva resumo em uma tabela de resumos
        pd.DataFrame([summary]).to_sql('traffic_summary', engine,
                                       if_exists='append', index=False)
        log.info(f"Resumo salvo na tabela 'traffic_summary'.")

        # Atualiza os registros originais como processados
        processed_ids = tuple(df['id'].tolist()) # Garante que 'id' existe e é lido
        if processed_ids:
            with engine.connect() as connection:
                update_query = text("UPDATE traffic_data SET is_transformed = TRUE WHERE id IN :ids")
                connection.execute(update_query, {"ids": processed_ids})
                connection.commit()
            log.info(f"{len(processed_ids)} registros marcados como transformados na tabela 'traffic_data'.")
        else:
            log.info("Nenhum ID para marcar como processado (verifique se a coluna 'id' está no DataFrame).")

    else:
        log.info("Nenhum dado novo para transformar.")

# Definição da DAG
with DAG(
    'pgcwb_dag',
    default_args=default_args,
    description='DAG para processamento de dados do PGCWB',
    # ATENÇÃO: Intervalo de 2 minutos ainda é MUITO FREQUENTE para APIs como Google Maps.
    # Verifique seus custos e cotas. Considere intervalos maiores (e.g., 15-60 minutos).
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['pgcwb', 'analise'],
) as dag:

    # Tarefa 1: Coleta de dados
    t1 = PythonOperator(
        task_id='collect_traffic_data',
        python_callable=_collect_traffic_data,
    )

    # Tarefa 2: Transformação dos dados
    t2 = PythonOperator(
        task_id='transform_data',
        python_callable=_transform_data,
    )

    # Definindo a ordem das tarefas
    t1 >> t2