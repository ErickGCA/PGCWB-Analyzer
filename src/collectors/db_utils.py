import os
import psycopg2
from dotenv import load_dotenv
# import json # Não mais necessário para a conversão redundante
import logging

load_dotenv()
log = logging.getLogger(__name__)

def insert_traffic_data(data: dict):
    """
    Insere um registro de dados de trânsito na tabela traffic_data.
    A tabela 'traffic_data' deve ter 'is_transformed' com DEFAULT FALSE.
    O campo 'id' deve ser SERIAL e será gerado automaticamente.
    """
    # data já é um dicionário, a conversão para JSON e de volta não é necessária.

    conn = None # Inicializa conn para garantir que existe no bloco finally
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        with conn: # Autocommit (ou rollback em caso de erro)
            with conn.cursor() as cur:
                # 'is_transformed' não precisa ser incluído aqui se tiver DEFAULT FALSE
                insert_query = """
                    INSERT INTO traffic_data (
                        timestamp, origin, destination, distance_meters, duration_seconds,
                        duration_in_traffic_seconds, start_lat, start_lng, end_lat, end_lng
                    ) VALUES (
                        %(timestamp)s, %(origin)s, %(destination)s, %(distance_meters)s,
                        %(duration_seconds)s, %(duration_in_traffic_seconds)s,
                        %(start_lat)s, %(start_lng)s, %(end_lat)s, %(end_lng)s
                    )
                """
                # Mapeia os dados do dicionário para o formato esperado pela query
                db_data = {
                    'timestamp': data['timestamp'],
                    'origin': data['origin'],
                    'destination': data['destination'],
                    'distance_meters': data['distance_meters'],
                    'duration_seconds': data['duration_seconds'],
                    'duration_in_traffic_seconds': data['duration_in_traffic_seconds'],
                    'start_lat': data['start_location']['lat'],
                    'start_lng': data['start_location']['lng'],
                    'end_lat': data['end_location']['lat'],
                    'end_lng': data['end_location']['lng']
                }
                cur.execute(insert_query, db_data)
        log.info("Dados de trânsito inseridos no banco de dados com sucesso.")
    except psycopg2.Error as e:
        log.error(f"Erro ao inserir dados no PostgreSQL: {e}")
        raise # Propaga a exceção para o Airflow
    except Exception as e:
        log.error(f"Erro inesperado em insert_traffic_data: {e}", exc_info=True)
        raise # Propaga a exceção para o Airflow
    finally:
        if conn:
            conn.close()